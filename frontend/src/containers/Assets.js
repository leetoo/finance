import React, { Component } from 'react';
import AssetsComponent from '../components/Assets'
import { connect } from 'react-redux'

const mapStateToProps = (state) => ({
  assets: state.assets.records,
  isFetching: state.assets.isFetching,
})

const Assets = connect(mapStateToProps)(AssetsComponent)

export default Assets
