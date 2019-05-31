import React, {Component} from 'react';
import './experience.scss'
import {reduxForm, FieldArray} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions';
import {connect} from "react-redux";
import moment from 'moment';
import validate from "../../../../../FormHandler/validtaions/experience/validate"
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderExperiences from "./renderExperience"
import {siteDomain} from "../../../../../../Utils/domains";
import AddSuggesion from '../../../../../Common/AddSuggestion/addSuggesion';
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"

class Experience extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.deleteExperience = this.deleteExperience.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false,
            'till_today': [],
            'modal_status':false,
            'scrollpos':'',
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);

    }
    componentDidMount() {
        this.props.fetchUserExperience()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_working)
        }
        this.setState({till_today})
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[2].entity_text})
        }
    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state
        till_today[parseInt(index)] = checked
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,2,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,2,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        this.setState({submit:true})
        currentLinkPos++
        await this.props.bulkUpdateUserExperience(values.list);
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
            const form_data = this.props.info.form.experience;
            let error = false
            let error_values =form_data["syncErrors"]
            if(error_values){
                for(let i of  error_values['list']){
                    for(let j of Object.keys(i)){
                        if(i[j]){
                            error =true
                            break;
                        }
                    }
                }
            }
            if(!error){
                const values = this.props.handleOrdering(form_data['values'])
                await this.props.bulkUpdateUserExperience(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[2].entity_text})
        }
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.is_working)
            }
            this.setState({till_today})
        }
    }

    async openModal(fields,index){

        const {job_profile:{label}} = fields.get(index)
        await this.props.fetchJobTitles(label,'experience')
        this.setState({modal_status:true,scrollpos:window.scrollY,fields,currentIndex:index})
    }

    closeModal(suggestions){
        console.log(suggestions)
        const {fields,currentIndex} = this.state
        const currentField = fields.get(currentIndex)
        if(Object.keys(suggestions).length){
            let suggestionsList = (currentField.work_description ? currentField.work_description + "\n" : '');
            Object.keys(suggestions).map((el,index) => {
                suggestionsList += suggestions[el] + (index+1 === Object.keys(suggestions).length ? "" : '\n')
            })
            currentField['work_description'] = suggestionsList;
            fields.remove(currentIndex);
            fields.insert(currentIndex, currentField)
        }
        this.setState({modal_status:false},()=>{ window.scrollTo(0, this.state.scrollpos)})
    }

    deleteExperience(index, fields, event) {
        event.stopPropagation();
        const experience = fields.get(index);
        fields.remove(index);
        if (experience && experience.id) {
            this.props.removeExperience(experience.id)
        }
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit,submitting,personalInfo:{subscription_status},history,previewHandling,
                changeOrderingUp,changeOrderingDown,fetchJobTitles,ui:{suggestions}} = this.props;
        const {editHeading,heading,till_today,modal_status} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <AddSuggesion label={'Job Description'} modal_status={modal_status} closeModal={this.closeModal} suggestions={suggestions}  />
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteExperience={this.deleteExperience}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                component={renderExperiences}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                heading ={heading}
                                context={this}
                                openModal={this.openModal}
                                till_today={till_today}
                                fetchJobTitles={fetchJobTitles}
                                tillTodayDisable={this.tillTodayDisable}/>
                    <ul className="form mt-15">
                        <li className="form__group">
                            <div className="btn-wrap">
                                 <button className="btn btn__round btn--outline" 
                                    onClick={async()=>{previewHandling(this.updateInfoBeforeLoss,history);this.setState({submit:true}) }}
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const ExperienceForm = reduxForm({
    form: 'experience',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'experience',-100),
    validate
})(Experience);


const mapStateToProps = (state) => {
    return {
        initialValues: state.experience,
        experience: state.experience,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userExperience) => {
            const {start_date, end_date} = userExperience;
            userExperience = {
                ...userExperience,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserExperience({userExperience, resolve, reject}));
            })
        },
        "fetchUserExperience": () => {
            return dispatch(actions.fetchUserExperience())
        },
        "removeExperience": (experienceId) => {
            return dispatch(actions.deleteExperience(experienceId))
        },
        "fetchJobTitles": (inputValue, suggestionType) => {
            if (inputValue.length < 3) return new Promise(resolve => resolve([]));
            return new Promise((resolve, reject) => {
                return dispatch(actions.fetchJobTitles({inputValue, suggestionType, resolve, reject}))
            })
        },

        "bulkUpdateUserExperience": (listItems) => {
            listItems = (listItems || []).map(userExperience => {
                const {start_date, end_date} = userExperience;
                if (!userExperience['id']) delete userExperience['id'];
                userExperience = {
                    ...userExperience,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null
                    }
                };
                return userExperience;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserExperience({list: listItems,resolve,reject}))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
