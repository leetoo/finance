import React, { Component } from 'react';
import PropTypes from 'prop-types';
import AssetLink from './AssetLink'
import { requestAssets } from '../actions'

class Assets extends Component {
  static propTypes = {
    dispatch: PropTypes.func.isRequired
  }

  componentDidMount() {
    const { dispatch } = this.props
    dispatch(requestAssets)
  }

  render() {
    console.log('Assets.render():', this.props)
    if (this.props.isFetching) {
      console.log('isFetching...')
      return (
        <div>
          <h2>Assets</h2>
          <div>Fetching assets...</div>
        </div>
      )
    }
    if (this.props.assets) {
      return (
        <div>
          <h2>Assets</h2>
          <ul>
            {this.props.assets.map(asset => <AssetLink key={asset.id} asset={asset}/>)}
          </ul>
        </div>
      );
    }
    else {
      return (<div>No asset is available</div>);
    }
  }
}

Assets.propTypes = {
  assets: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      code: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired
    }).isRequired
  ).isRequired
}

export default Assets
