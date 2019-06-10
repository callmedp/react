import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
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
import {scrollOnErrors} from "../../../../../../Utils/srollOnError";

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
        console.log("Here")
        if(!this.state.submit){
            const form_data = this.props.info.form.personalInfo;
            let error = false
            let error_values =form_data["syncErrors"]
            if(error_values){
                for(let i of  Object.keys(error_values)){
                    if(error_values[i]){
                        error =true;
                        break;
                    }
                }
            }
            if(!error){
                await this.props.onSubmit(form_data['values']);
            }
        }
        
    }

    async componentWillUnmount() {
        this.updateInfoBeforeLoss();
    }

    

    

    async handlePreview() {
        
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
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
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

        this.setState({
            'imageURL': url,
            flag:true
        })
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit, personalInfo,submitting,personalInfo:{subscription_status},history} = this.props;
        const {editHeading,heading,flag} =this.state;
        return (
            
        <div className="buildResume">
            <PreviewModal {...this.props}/>
            <div className="buildResume__wrap">
                <div className="buildResume__heading">
                    {!editHeading ?
                        
                        <React.Fragment>
                            <h1>{heading}</h1>
                            <i className="sprite icon--edit" onClick={()=>{this.setState({editHeading:true})}}></i>
                            {/* <div className="toolTip">
                                <span className="toolTip--arrow-up"></span>
                                <span className="toolTip--close">+</span>
                                You can always edit the section title
                            </div> */}
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} onBlur={(e)=>this.updateInputValue('blur',e)}
                                onKeyDown={(e)=>this.updateInputValue('keyPress',e)} maxLength="20"/>
                            <i className="sprite icon--editTick"></i>
                        </React.Fragment>
                         
                    }
                    {/*  */}
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
                             yearDropDownItemNumber={50} pattern="\d*"  readOnly/>
                        </li>

                        <li className="form__group">
                            <Field component={renderField} label={"Mobile"}  type={"number"} name="number" id="number" prepend={true}
                                iconClass={"sprite icon--mobile"} className="form__input" pattern="\d*" maxLength="10"/>
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
                            {
                                (this.state.imageURI || personalInfo.image) && flag ?
                                    <React.Fragment>
                                        <span className="close-wrap">
                                            <i className="sprite icon--close" onClick={()=>{this.setState({imageURL:'',imageURI:'',flag:false})}}></i>
                                        </span>
                                        <img alt={"User Profile"}
                                                src={this.state.imageURI || personalInfo.image}/> 
                                    </React.Fragment>:
                                    <img alt={"User Profile"}
                                            src="/media/static/react/assets/images/mobile/default-user.jpg"/>
                            }
                            </span>
                        </li>
                    </ul>
                    <BottomCTC  disabled={submitting} context={this} history={history}
                                length={length} pos={pos+1} updateInfoBeforeLoss={this.updateInfoBeforeLoss} 
                                subscription_status={subscription_status}/>
                </form>
            </div>
            
        </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'profile',-100),
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
            let { date_of_birth, extracurricular,gender} = personalDetails;
            let interest = extracurricular
            interest =  ((interest|| []).filter((item)=>item !==null).map((item)=>item.value)).join(",")
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'image': imageURL || personalDetails['image'],
                    'extracurricular':interest,
                    'gender' : gender
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
