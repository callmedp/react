import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import './summary.scss';



import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import PreviewModal from "../../../Preview/changeTemplateModal";

import validate from "../../../../../FormHandler/validtaions/summary/validate"
import {siteDomain} from "../../../../../../Utils/domains";


class Summary extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
    }

    componentDidMount() {
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[5].entity_text})
        }

    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,5,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,5,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[5].entity_text})
        }
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        this.setState({submit:true})
        await this.props.onSubmit(values);
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
            const form_data = this.props.info.form.summary;
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
                this.setState({submit:true})
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {personalInfo: {subscription_status}, handleSubmit,submitting,history,previewHandling} = this.props;
        const {editHeading,heading} =this.state;
        return (
        <div className="buildResume">
            <PreviewModal {...this.props}/>
            
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading">
                {!editHeading ?
                        <React.Fragment>
                            <h1>{heading}</h1>
                            <i className="sprite icon--edit" onClick={()=>{this.setState({editHeading:true})}}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} onBlur={(e)=>this.updateInputValue('blur',e)}
                                onKeyDown={(e)=>this.updateInputValue('keyPress',e)}/>
                            <i className="sprite icon--editTick"></i>
                        </React.Fragment>
                         
                    }
                </div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <ul className="form">
                    
                        <li className="form__group">
                            <Field component={renderTextArea} label={"Summary"}  type={"text"} name="extra_info" 
                                id="extra_info" prepend={false} className="form__input h-150"/>
                            {/* <p className="add-suggested" onClick={this.handleOpenModal}>
                                <span>+</span>Add suggested summary
                            </p> */}
                        </li>
                    </ul>
                    <div className="btn-wrap">
                        <button className="btn btn__round btn--outline" 
                            onClick={async()=>{previewHandling(this.updateInfoBeforeLoss,history) }}
                            type={'button'}>Preview</button>
                        <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                            {(length === pos +1) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                        </button>
                    </div>
                </form>
                
            </div>
        </div>
        )
    }
}

export const SummaryForm = reduxForm({
    form: 'summary',
    enableReinitialize: true,
    validate
})(Summary);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails
            personalDetails = {
                ...personalDetails,
                ...{
                    'gender': gender && gender['value'] || '',
                    'extracurricular':''
                    // 'extracurricular': (extracurricular || []).map(el => el.value).join(',')
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SummaryForm);
