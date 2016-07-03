from datetime import datetime, timedelta

from logbook import Logger
from typedecorator import typed

# NOTE: finance.models should not be imported here in order to avoid circular
# depencencies

log = Logger('finance')


def date_range(start, end, step=1):
    """Generates a range of dates.

    :param start: Starting date (inclusive)
    :param end: Ending date (exclusive)
    :param step: Number of days to jump (currently unsupported)
    """
    if step != 1:
        raise NotImplementedError('Any value of step that is not 1 is not '
                                  'supported at the moment')

    if isinstance(start, str) or isinstance(start, int):
        start = parse_date(start)

    if isinstance(end, str) or isinstance(end, int):
        end = parse_date(end)

    if start > end:
        raise ValueError('Start date must be smaller than end date')

    delta = end - start
    for i in range(0, delta.days):
        yield start + timedelta(days=i)


def extract_numbers(value, type=str):
    """Extracts numbers only from a string."""
    def extract(vs):
        for v in vs:
            if v in '01234567890.':
                yield v
    return type(''.join(extract(value)))


def parse_date(date, format='%Y-%m-%d'):
    """Make a datetime object from a string.

    :type date: str or int
    """
    if isinstance(date, int):
        return datetime.now().date() + timedelta(days=date)
    else:
        return datetime.strptime(date, format)


def parse_decimal(v, type=float):
    try:
        return type(v)
    except ValueError:
        return None


def parse_int(v):
    """Parses a string as an integer value. Falls back to zero when failed to
    parse."""
    try:
        return int(v)
    except ValueError:
        return 0


def parse_nullable_str(v):
    return v if v else None


def parse_stock_code(code: str):
    """Parses a stock code. NOTE: Only works for the Shinhan HTS"""
    if code.startswith('A'):
        return code[1:]
    elif code == '':
        return None
    else:
        return code


def parse_stock_data(stream):
    """
    :param stream: A steam to read in a CSV file.
    """
    first_header, second_header = next(stream), next(stream)
    while True:
        try:
            first_line, second_line = next(stream), next(stream)
        except StopIteration:
            break

        cols1 = first_line.split('\t')[:13]
        cols2 = second_line.split('\t')[:12]

        date, category1, code, quantity, subtotal, 미수발생_변제, interest, \
            fees, late_fees, 상대처, 변동금액, 대출일, 처리자 = cols1

        상품, category2, name, unit_price, 신용_대출금, 신용_대출이자, \
            예탁금이용료, 제세금, channel, 의뢰자명, final_amount, 만기일 \
            = cols2

        # NOTE: Date is in some peculiar format as following:
        #
        #     20160222000000000000000003
        #     20160222000000000000000002
        #     20160222000000000000000001
        #
        # where '20160202' is a date (YYYYMMDD) and the tailing number
        # appears to be the sequence of the day. In this case, the first row
        # indicates the transaction was the third one on 2016-02-02.
        date, sequence = parse_date(date[:8], '%Y%m%d'), int(date[8:])

        yield {
            'date': date,
            'sequence': sequence,
            'category1': category1,
            'category2': category2,
            'code': parse_stock_code(code),
            'name': name,
            'unit_price': parse_int(unit_price),
            'quantity': parse_int(quantity),
            'subtotal': parse_int(subtotal),
            'interest': parse_int(interest),
            'fees': parse_int(fees),
            'late_fees': parse_int(late_fees),
            'channel': channel,
            'final_amount': parse_int(final_amount),
        }


def insert_stock_record(data: dict):
    """
    account_id = db.Column(db.BigInteger, db.ForeignKey('account.id'))
    asset_id = db.Column(db.BigInteger, db.ForeignKey('asset.id'))
    # asset = db.relationship(Asset, uselist=False)
    transaction_id = db.Column(db.BigInteger, db.ForeignKey('transaction.id'))
    type = db.Column(db.Enum(*record_types, name='record_type'))
    # NOTE: We'll always use the UTC time
    created_at = db.Column(db.DateTime(timezone=False))
    category = db.Column(db.String)
    quantity = db.Column(db.Numeric(precision=20, scale=4))
    """
    from finance.models import get_asset_by_stock_code, Record

    if data['category1'].startswith('장내'):
        code_suffix = '.KS'
    elif data['category1'].startswith('코스닥'):
        code_suffix = '.KQ'
    else:
        raise ValueError(
            "code_suffix could not be determined with the category '{}'"
            ''.format(data['category1']))

    code = data['code'] + code_suffix

    asset = get_asset_by_stock_code(code)
    if asset is None:
        raise ValueError(
            "Asset object could not be retrived with code '{}'".format(code))

    return Record.create(
        created_at=data['date'],
        quantity=data['quantity'],
        asset=asset,
    )


def import_8percent_data(parsed_data, account_checking, account_8p, asset_krw):
    from finance.models import Asset, AssetType, AssetValue, Record, \
        Transaction

    assert account_checking
    assert account_8p
    assert asset_krw

    parsed_data = DictReader(parsed_data)
    asset_data = {
        'started_at': parsed_data.started_at.isoformat()
    }
    keys = ['annual_percentage_yield', 'amount', 'grade', 'duration',
            'originator']
    for key in keys:
        asset_data[key] = parsed_data[key]

    asset_8p = Asset.create(name=parsed_data.name, type=AssetType.p2p_bond,
                            data=asset_data)
    remaining_value = parsed_data.amount
    started_at = parsed_data.started_at

    with Transaction.create() as t:
        Record.create(
            created_at=started_at, transaction=t, account=account_checking,
            asset=asset_krw, quantity=-remaining_value)
        Record.create(
            created_at=started_at, transaction=t, account=account_8p,
            asset=asset_8p, quantity=1)
    AssetValue.create(
        evaluated_at=started_at, asset=asset_8p,
        base_asset=asset_krw, granularity='1day', close=remaining_value)

    for record in parsed_data.records:
        date, principle, interest, tax, fees = record
        returned = principle + interest - (tax + fees)
        remaining_value -= principle
        with Transaction.create() as t:
            Record.create(
                created_at=date, transaction=t,
                account=account_checking, asset=asset_krw, quantity=returned)
        AssetValue.create(
            evaluated_at=date, asset=asset_8p,
            base_asset=asset_krw, granularity='1day', close=remaining_value)


def insert_asset(row, data=None):
    """Parses a comma separated values to fill in an Asset object.
    (type, name, description)

    :param row: comma separated values
    """
    from finance.models import Asset
    type, name, description = [x.strip() for x in row.split(',')]
    return Asset.create(
        type=type, name=name, description=description, data=data)


def insert_asset_value(row, asset, base_asset):
    """
    (evaluated_at, granularity, open, high, low, close)
    """
    from finance.models import AssetValue
    columns = [x.strip() for x in row.split(',')]
    evaluated_at = parse_date(columns[0])
    granularity = columns[1]
    open, high, low, close = map(parse_decimal, columns[2:6])
    return AssetValue.create(
        asset=asset, base_asset=base_asset, evaluated_at=evaluated_at,
        granularity=granularity, open=open, high=high, low=low, close=close)


def insert_record(row, account, asset, transaction):
    """
    (type, created_at, cateory, quantity)
    """
    from finance.models import Record
    type, created_at, category, quantity = [x.strip() for x in row.split(',')]
    type = parse_nullable_str(type)
    created_at = parse_date(created_at)
    category = parse_nullable_str(category)
    quantity = parse_decimal(quantity)
    return Record.create(
        account=account, asset=asset, transaction=transaction, type=type,
        created_at=created_at, category=category, quantity=quantity)


class AssetValueImporter(object):
    pass


class DictReader(object):
    def __init__(self, value):
        if not isinstance(value, dict):
            raise ValueError('DictReader only accepts dict type')
        self.value = value

    def __getattr__(self, name):
        return self.value[name]

    def __getitem__(self, key):
        return self.value[key]
