import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { requestAsset } from '../actions'

class AssetView extends Component {
  static propTypes = {
    asset: PropTypes.shape({
      id: PropTypes.string.isRequired,
      code: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired
    }).isRequired,
    dispatch: PropTypes.func.isRequired
  }

  componentDidMount() {
    const { dispatch } = this.props
    dispatch(requestAsset)
  }

  render() {
    console.log('AssetView.render():', this.props)
    const { asset } = this.props
    if (asset) {
      return (
        <div>
          <h2>Asset {asset.code} {asset.name}</h2>
        </div>
      )
    }
    else {
      return (
        <div>
          <h2>Unknown Asset</h2>
        </div>
      )
    }
  }
}

export default AssetView
