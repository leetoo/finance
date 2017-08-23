import React, { Component } from 'react';
import PropTypes from 'prop-types';

class AssetLink extends Component {
  static propTypes = {
    asset: PropTypes.shape({
      id: PropTypes.string.isRequired,
      code: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired
    }).isRequired,
  }

  render() {
    const { asset } = this.props
    return (
      <div>
        <a href={'/assets:' + asset.id}>{asset.code} ({asset.name})</a>
      </div>
    )
  }
}

export default AssetLink
