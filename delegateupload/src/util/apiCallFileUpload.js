const api_url = 'http://127.0.0.1:5000'

function apiCallFileUpload(endpoint, method='post', data=null){
    const url = api_url + endpoint
    let formData = new FormData()
    formData.append("filename", data)
    console.log(url)
    console.log(data)
    console.log(formData)
    const options = {
        method: 'POST', 
        mode: "cors",       
        body: data
        
      };
      if (options && options.headers) {
        delete options.headers['Content-Type'];
      }
    
      return fetch(url, options).then(response => response.json())
    

}

export default apiCallFileUpload