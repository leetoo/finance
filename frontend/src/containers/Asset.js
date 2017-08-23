import React, { Component } from 'react';
import AssetView from '../components/AssetView'
import { connect } from 'react-redux'

const mapStateToProps = (state) => ({
  asset: state.asset.record,
  isFetching: state.asset.isFetching,
})

const Asset = connect(mapStateToProps)(AssetView)

export default Asset
