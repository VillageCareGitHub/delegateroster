import React from "react";

import apiCall from '../util/apiCallFileUpload';

import PropTypes from "prop-types";

import withStyles from "@material-ui/core/styles/withStyles";

import GridItem from "../components/Grid/GridItem.jsx";
import GridContainer from "../components/Grid/GridContainer.jsx";
import CustomInput from "../components/CustomInput/CustomInput.jsx";
import Button from "../components/CustomButtons/Button.jsx";

import Card from "../components/Card/Card.jsx";
import CardHeader from "../components/Card/CardHeader.jsx";
import CardBody from "../components/Card/CardBody.jsx";

import Select from "react-select";

import "../css/maincss.css";


const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none"
  }
};

const facilities=[{value:'ifh',label:'Institute for Family Health'},
{value:'integrap',label:'Integra Partners'},
{value:'ecap',label:'Eastern Chinese American IPA'},];

class UploadDelegateRoster extends React.Component {
  state={
    filetoupload:null,
    fileresponse:null,
    fileresponsedata:null
}

uploadFile(e) {
    e.preventDefault();
    let file = this.state.filetoupload;
    
    let formData = new FormData()
    let name = "ex"; // Just an example
    let url='http://127.0.0.1:5000/api/delegateroster/importfile'
    formData.append("filename", file)
    let xhr = new XMLHttpRequest()
    xhr.responseType='text'
    console.log(formData)
    xhr.open('POST', url, true)
    xhr.send(formData)
    xhr.addEventListener("load", function() {
        console.log(this.responseText)
    })
    console.log('about to see response')
    console.log(xhr.response)
    
    // console.log(JSON.stringify(xhr.responseText))
    this.setState({
        fileresponse:'File Uploaded'
    })
  }






  render() {
    const { classes } = this.props;
  



  return (
    <div className="mainpage">
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="success">
              <h4 className={classes.cardTitleWhite}>Import Provider Delegate Roster</h4>
              <p className={classes.cardCategoryWhite}>Importing delegate rosters to translate and save to ILS (Independent Living Systems) folder for upload</p>
            </CardHeader>
            <CardBody>
              <div className="fileselector">
              <GridContainer>
                <GridItem xs={12} sm={12} md={10}>
                  <CustomInput
                    labelText=""
                    id="filename"
                    formControlProps={{
                      fullWidth: true
                    }}
                    inputProps={{
                      disabled: false,
                      type:"file"
                    }}
                    onChange={(event)=>{
                      console.log(event.target.files[0])
                      window.sessionStorage.setItem("uploadfile", event.target.files[0].name);
                      this.setState({
                          filetoupload:event.target.files[0]
                      })}}
                  />
                </GridItem> 
                <GridItem xs={12} sm={12} md={4}>
                <div className="facilityselector">
                  <label>Select Facility to Map to File</label><Select id="facility" placeholder='SELECT DELEGATE ROSTER FACILITY'
                  options={facilities}>Select Delegate Roster Facility</Select>
                </div>
                </GridItem>      
                
              </GridContainer>
              <GridContainer>
                <GridItem xs={12} sm={12} md={4}>
                <div className="customimportbutton"><Button onClick={(event)=>{                 
                    
                    this.uploadFile(event)
                    alert('Provider Roster Uploaded')
                    
                }}>Upload Provider Roster</Button></div>
                </GridItem>
              </GridContainer>
              </div>
            </CardBody>
           
          </Card>
        </GridItem>
        
      </GridContainer>

      
    </div>
  );
}
}

UploadDelegateRoster.propTypes = {
  classes: PropTypes.object
};

export default withStyles(styles)(UploadDelegateRoster);
