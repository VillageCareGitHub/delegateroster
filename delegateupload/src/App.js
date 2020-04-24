import React, { Component } from 'react';
import {BrowserRouter, Route} from "react-router-dom"
import './App.css';

import UploadPage from "./views/upload_delegate_roster"

class App extends Component {

  render(){
    let routelist=[]
    
    routelist=[<Route exact path="/" component={UploadPage}/>]

  return (
    <BrowserRouter>
      <div>
        <main>
         <a>href={routelist}>Click Here</a>
        </main>
      </div>
    
    </BrowserRouter>
    
  );
}
}

export default App;
