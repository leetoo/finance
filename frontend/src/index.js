import React from 'react';
// import ReactDOM from 'react-dom';
import { render } from 'react-dom'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import thunk from 'redux-thunk'
import './index.css';
import App from './App'
import Asset from './containers/Asset'
import Assets from './containers/Assets'
import reducer from './reducers'
import registerServiceWorker from './registerServiceWorker'

const middleware = [ thunk ]

let store = createStore(
  reducer,
  applyMiddleware(...middleware)
)

render(
  <Provider store={store}>
    <Router>
      <div>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/assets">Assets</Link></li>
        </ul>
        <Route exact path="/" component={App}/>
        <Route exact path="/assets" component={Assets}/>
        <Route path="/assets:id" component={Asset}/>
      </div>
    </Router>
  </Provider>,
  document.getElementById('root')
)
