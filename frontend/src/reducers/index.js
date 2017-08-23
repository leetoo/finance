import { combineReducers } from 'redux'
import {
  ASSETS_REQUEST, ASSETS_RECEIVED,
  ASSET_RECEIVED
} from '../actions'


const initialState = {
  isFetching: true,
  didInvalidate: false,
  records: [],
  error: null
}

const assets = (state = initialState, action) => {
  console.log('recuder: state=', state, ', action=', action)
  switch (action.type) {
    case ASSETS_REQUEST:
      return {
        ...state,
        isFetching: true
      }
    case ASSETS_RECEIVED:
      return {
        ...state,
        isFetching: false,
        records: action.assets.records
      }
    default:
      return state
  }
}

const initialAssetState = {
  isFetching: true,
  didInvalidate: false,
  record: null,
  error: null
}

const asset = (state = initialAssetState, action) => {
  console.log('recuder: state=', state, ', action=', action)
  switch (action.type) {
    case ASSET_RECEIVED:
      console.log(action.asset)
      return {
        ...state,
        isFetching: false,
        record: action.asset
      }
    default:
      return state
  }
}

const rootReducer = combineReducers({
  assets, asset
})

export default rootReducer
