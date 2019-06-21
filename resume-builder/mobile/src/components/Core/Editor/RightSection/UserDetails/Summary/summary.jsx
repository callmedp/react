import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import './summary.scss';
import {fetchJobTitles,fetchUserExperience} from '../../../../../../store/experience/actions/index';

import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import PreviewModal from "../../../Preview/changeTemplateModal";
import moment from 'moment'
import validate from "../../../../../FormHandler/validtaions/summary/validate"
import {siteDomain} from "../../../../../../Utils/domains";
import AddSuggesion from '../../../../../Common/AddSuggestion/addSuggesion';
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';


class Summary extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false,
            'modal_status':false,
            'summary' :''
        }
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserExperience()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[5].entity_text})
        }

    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[5].entity_text})
        }
    }

    async handleSubmit(values) {
        let {sidenav:{listOfLinks,currentLinkPos},onSubmit,personalInfo:{order_data},updateCurrentLinkPos,history,showGenerateResumeModal,hideGenerateResumeModal,reGeneratePDF} = this.props
        currentLinkPos++
        this.setState({submit:true})
        await onSubmit(values);
         if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            if(order_data && order_data.id){
                showGenerateResumeModal()
                reGeneratePDF(order_data.id)
                setTimeout(function() {
                    window.location.href = `${siteDomain}/dashboard`
                    hideGenerateResumeModal()
                }, 10000);
            }
            else{
                history.push(`/resume-builder/buy`) 
            }
        }
        else{
            updateCurrentLinkPos({currentLinkPos})
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    async openModal(){
        const {experience} = this.props;
        let latest_experience = ''
        let  latest_end_date = 'None'
        for (let exp of experience.list){
            if (exp.is_working){
                latest_experience = exp.job_profile
                break
            }
            else if(latest_end_date === 'None'){
                latest_end_date = exp.end_date
                latest_experience = exp.job_profile
            }
            else{
                if( latest_end_date < exp.end_date){
                    latest_end_date = exp.end_date
                    latest_experience = exp.job_profile
                }
                    
            }
                
        }
            
        let label = latest_experience && latest_experience.label
        await this.props.fetchJobTitles(label,'summary')
        this.setState({modal_status:true})
    }

    closeModal(suggestions){
        const {personalInfo:{extra_info},upateSummaryWithSuggestion} = this.props
        if(Object.keys(suggestions).length){
            let suggestionsList = (extra_info ? extra_info + "\n" : '');
            Object.keys(suggestions).map((el,index) => {
                suggestionsList += suggestions[el] + (index+1 === Object.keys(suggestions).length ? "" : '\n')
            })
            upateSummaryWithSuggestion(suggestionsList)
        }
        this.setState({modal_status:false})
    }

    async updateInfoBeforeLoss(){

        if(!this.state.submit){
            const {initialValues} =this.props
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
            if(!error && JSON.stringify(initialValues)!==JSON.stringify(form_data['values'])){
                
                await this.props.onSubmit(form_data['values']);
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {personalInfo: {order_data,entity_preference_data},extra_info,headingChange, handleSubmit,submitting,history,ui:{suggestions},updateAlertModalStatus} = this.props;
        const {editHeading,heading,modal_status} =this.state;
        return (
        <div className="buildResume">
            <PreviewModal {...this.props}/>
            <AddSuggesion label={'Summary'} modal_status={modal_status} length={extra_info.length} maxLength="500" closeModal={this.closeModal} suggestions={suggestions}/>
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading">
                {!editHeading ?
                        <React.Fragment>
                            <h1 className="heading-style">{heading}</h1>
                            <i className="sprite icon--edit" onClick={()=>{this.setState({editHeading:true})}}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} maxLength={'20'}
                                    onChange={(event) => this.setState({heading:event.target.value})} />
                            <i className="sprite icon--editTick" 
                                onClick={()=>{headingChange(entity_preference_data,heading,5);this.setState({editHeading:false})}}></i>
                        </React.Fragment>
                         
                    }
                </div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <ul className="form">
                    
                        <li className="form__group">
                            <Field component={renderTextArea} label={"Summary"}  type={"text"} name="extra_info" 
                                id="extra_info" prepend={false} className="form__input h-150" maxLength={"500"}/>
                            <p className="add-suggested" onClick={()=>{this.openModal()}}>
                                <span>+</span>Add suggested summary
                            </p>
                        </li>
                    </ul>
                    <BottomCTC  disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
                                length={length} pos={pos+1} updateInfoBeforeLoss={this.updateInfoBeforeLoss} 
                                order_data={order_data}/>
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
        personalInfo: state.personalInfo,
        ui: state.ui,
        experience: state.experience,
        extra_info: state.form && state.form.summary &&  state.form.summary.values &&  state.form.summary.values.extra_info || ''
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "upateSummaryWithSuggestion": (data) => {
            return dispatch(actions.upateSummaryWithSuggestion(data))
        },
        "onSubmit": (personalDetails) => {
            let { date_of_birth, extracurricular,gender,image} = personalDetails;
            let interest = extracurricular
            interest =  ((interest|| []).filter((item)=>item !==null).map((item)=>item.value)).join(",")
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'image': image,
                    'extracurricular':interest,
                    'gender' : gender
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "fetchJobTitles": (inputValue, suggestionType) => {
            if (inputValue.length < 3) return new Promise(resolve => resolve([]));
            return new Promise((resolve, reject) => {
                return dispatch(fetchJobTitles({inputValue, suggestionType, resolve, reject}))
            })
        },
        "fetchUserExperience": () => {
            return dispatch(fetchUserExperience())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SummaryForm);
