import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';

import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import PreviewModal from "../../../Preview/previewModal";


class Summary extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : ''
        }
        this.updateInputValue =this.updateInputValue.bind(this);
    }

    componentDidMount() {
        this.props.fetchPersonalInfo()
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
                console.log("came here")
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
        await this.props.onSubmit(values);
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            this.props.history.push(`/resume-builder/buy`)
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
        
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {personalInfo: {extra_info}, handleSubmit,submitting,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        return (
        <div className="buildResume">
            <PreviewModal {...this.props}/>
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading">
                    {!editHeading ?
                        <h1>{heading}</h1>:
                        <input autoFocus type="text" id="heading" placeholder={heading} onBlur={(e)=>this.updateInputValue('blur',e)}
                         onKeyDown={(e)=>this.updateInputValue('keyPress',e)}/>
                    }
                    <i className="sprite icon--edit" onClick={()=>{this.setState({editHeading:true})}}></i>
                </div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <ul className="form">
                    
                        <li className="form__group">
                            <Field component={renderTextArea} label={"Summary"}  type={"text"} name="extra_info" 
                                id="extra_info" prepend={false} className="form__input h-300"/>
                        </li>
                        
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ?"Buy" :"Save & Continue"}
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

export const SummaryForm = reduxForm({
    form: 'summary',
    enableReinitialize: true
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
