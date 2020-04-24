const api_url = 'http://127.0.0.1:5000'

function apiCall(endpoint, method='get', data=null) {
    const url = api_url + endpoint
    if (method === 'get') {
        return fetch(url, {
            method: 'get',
            mode: 'cors'
            
        })
    }
    else {
        return fetch(url, {
            method: method,
            mode: "cors",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        })
    }
}



export default apiCall