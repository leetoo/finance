export const ASSETS_REQUEST = 'ASSETS_REQUEST'
export const ASSETS_RECEIVED = 'ASSETS_RECEIVED'
export const ASSETS_FAILED = 'ASSETS_FAILED'

export const ASSET_REQUEST = 'ASSET_REQUEST'
export const ASSET_RECEIVED = 'ASSET_RECEIVED'
export const ASSET_FAILED = 'ASSET_FAILED'

const API_ROOT = 'http://52.78.101.90:8002'

export const requestAssets = dispatch => {
  return fetch(`${API_ROOT}/entities/asset`)
    .then(response => response.json())
    .then(json => dispatch(receiveAssets(json)))
    .catch(err => { fetchFailed(err) })
}

export function receiveAssets(assets) {
  return {type: ASSETS_RECEIVED, assets: assets}
}

// TODO: Change a function name
export function fetchFailed(error) {
  return {type: ASSETS_FAILED, error: error}
}

export const requestAsset = dispatch => {
  return fetch(`${API_ROOT}/entities/asset`)
    .then(response => response.json())
    .then(json => dispatch(receiveAsset(json)))
    .catch(err => { fetchFailed(err) })
}

export function receiveAsset(assets) {
  //console.log('receiveAssets: ', assets.records[0])
  return {type: ASSET_RECEIVED, asset: assets.records[0]}
}
