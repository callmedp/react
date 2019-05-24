import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {interestList} from '../../../../../../Utils/interestList';
import './personalInfo.scss';
import {
    renderField,
    datepicker,
    renderSelect,
    renderTextArea,
    renderMultiselect
} from "../../../../../FormHandler/formFieldRenderer.jsx";

import moment from 'moment';
import PreviewModal from "../../../Preview/changeTemplateModal";
import validate from "../../../../../FormHandler/validtaions/profile/validate"
import {siteDomain} from "../../../../../../Utils/domains";
import DataLoader from '../../../../../Common/DataLoader/dataloader';

class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePreview = this.handlePreview.bind(this);
        this.state = {
            'imageURI': '',
            'imageURL': '',
            'editHeading': false,
            'heading' : '',
            'submit': false
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)


    }

    componentDidMount() {
        this.props.fetchInterestList();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[0].entity_text})
        }
        
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        this.setState({submit:true})
        await this.props.onSubmit(values, this.state.imageURL);
         if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            if(this.props.personalInfo.subscription_status){
                window.location.href = `${siteDomain}/dashboard/myorder`
            }
            else{
                this.props.history.push(`/resume-builder/buy`) 
            }
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    async updateInfoBeforeLoss(){
        if(!this.state.submit){
            const form_data = this.props.info.form.personalInfo;
            // console.log(form_data)
            let error = false
            let error_values =form_data["syncErrors"]
            // console.log(error_values)
            if(error_values){
                for(let i of  Object.keys(error_values)){
                    if(error_values[i]){
                        error =true;
                        break;
                    }
                }
            }
            if(!error){
                await this.props.onSubmit(form_data['values'],this.state.imageURL);
                this.setState({submit:true})
            }
        }
        
    }

    async componentWillUnmount() {
        this.updateInfoBeforeLoss();
    }

    

    

    handlePreview() {
        this.props.history.push('/resume-builder/preview/');
    }

    removeImage() {
        this.setState({
            imageURI: '',
            imageURL: ''
        })
    }


    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[0].entity_text})
            // console.log("Came Inside")
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
                // console.log("update value")
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
                // console.log("blur value")
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }


    async getImageURI(event) {
        let reader = new FileReader();
        reader.onload = (event) => {

            this.setState({
                imageURI: event.target.result
            })

        };
        reader.readAsDataURL(event.target.files[0]);

        let url = await this.props.fetchImageUrl(event.target.files[0]);
        ////console.log(url)

        this.setState({
            'imageURL': url
        })
    }
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit, personalInfo,submitting,previewHandling,history,loader:{dataloader}} = this.props;
        const {editHeading,heading} =this.state;
        const {subscription_status} = this.props.personalInfo;
        return (
            
        <div className="buildResume">
            {dataloader ?<DataLoader/> : ""}
            <PreviewModal {...this.props}/>
            <div className="buildResume__wrap">
            {/* {this.props.loader.dataloader ?  <DataLoader/> :""} */}
                <div className="buildResume__heading">
                    {!editHeading ?
                        <h1>{heading}</h1>:
                        <input type="text" autoFocus placeholder={heading} onBlur={(e)=>this.updateInputValue('blur',e)}
                         onKeyDown={(e)=>this.updateInputValue('keyPress',e)}/>
                    }
                    <i className="sprite icon--edit" onClick={()=>{this.setState({editHeading:true})}}></i>
                </div>
                
                
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    
                    <ul className="form">

                        <li className="form__group">
                            <Field component={renderField} label={"First Name"}  type={"text"} name="first_name" id="first_name"
                                iconClass={"sprite icon--firstName"}  className="form__input" prepend={true}/>
                        </li>

                        <li className="form__group">
                            <Field component={renderField} label={"Last Name"}  type={"text"} name="last_name" id="last_name"
                                iconClass={"sprite icon--lastName"} className="form__input" prepend={true}/>
                        </li>

                        <li className="form__group">
                            <Field component={renderSelect} label={"Gender"} name="gender" name="gender" prepend={true}
                                iconClass={"sprite icon--designation"}  className="form__input form__select">
                                <option value="">Gender</option>
                                <option value="1" >Male</option>
                                <option value="2" >Female</option>
                                <option value="3">Others</option>
                            </Field>
                        </li>
                        
                        <li className="form__group">
                            <Field component={datepicker} label={"Date Of Birth"}  type={"date"} name="date_of_birth" id="date_of_birth"
                             yearDropDownItemNumber={50}/>
                        </li>

                        <li className="form__group">
                            <Field component={renderField} label={"Mobile"}  type={"text"} name="number" id="number" prepend={true}
                                iconClass={"sprite icon--mobile"} className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={renderField} label={"Email"}  type={"email"} name="email" id="email" prepend={true}
                                iconClass={"sprite icon--mail"}  className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={renderTextArea} label={"Address"}  type={"text"} name="location" id="location" 
                                prepend={true} iconClass={"sprite icon--address"} className="form__input" rows="4"/>
                        </li>

                        <li className="form__group">
                            <Field name="extracurricular" component={renderMultiselect} data={Object.values(personalInfo.interest_list)}
                                    valueField='value' textField='label' className={'multi-select'}
                                    defaultValue={personalInfo.extracurricular}
                            />
                        </li>

                        <li className="form__group">
                            <div className="upload-btn-wrapper">

                                <button className="upload-btn-wrapper__btn">
                                    <i className="sprite icon--camera"></i>
                                    Upload a file
                        </button>
                                <input type="file" accept="image/*" name="displayPicture"
                                       onChange={this.getImageURI.bind(this)} />
                            </div>
                        </li>

                        <li className="form__group">
                            <span className="upload--image">
                            <span className="close-wrap">
                                <i className="sprite icon--close"></i>
                            </span>
                            {
                                this.state.imageURI || personalInfo.image ?
                                    <img alt={"User Profile"}
                                            src={this.state.imageURI || personalInfo.image}/> :
                                    <img alt={"User Profile"}
                                            src="/media/static/react/assets/images/mobile/default-user.jpg"/>
                            }
                            </span>
                        </li>

                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={async()=>{previewHandling(this.updateInfoBeforeLoss,history) }}
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true,
    validate
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (personalDetails, imageURL) => {

            let { date_of_birth, extracurricular} = personalDetails;
            let interest = extracurricular
            interest =  ((interest|| []).map((item)=>item.value)).join(",")
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'image': imageURL,
                    'extracurricular':interest
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "fetchImageUrl": (imageFile) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.fetchImageUrl({imageFile, resolve, reject}));
            })
        },
        "fetchInterestList": () => {
                dispatch(actions.fetchInterestList());
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
