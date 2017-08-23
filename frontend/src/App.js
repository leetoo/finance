import React, { Component } from 'react';
import { connect } from 'react-redux'
import PropTypes from 'prop-types';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  static propTypes = {
    dispatch: PropTypes.func.isRequired
  }

  componentDidMount() {
    const { dispatch } = this.props
  }

  render() {
    return (
      <div>
        <p>This is our main app</p>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {}
}

export default connect(mapStateToProps)(App)
