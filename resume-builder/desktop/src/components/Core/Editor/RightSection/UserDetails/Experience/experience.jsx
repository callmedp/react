import React, {Component} from 'react';
import {reduxForm, FieldArray} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions/index';
import {connect} from "react-redux";
import moment from 'moment';
import {ExperienceRenderer} from "./experienceRenderer";
import validate from '../../../../../FormHandler/validations/experience/validate'
import {scroller} from "react-scroll/modules";
import SuggestionModal from '../../../../../Modal/suggestionModal'
import {hideSuggestionModal, showSuggestionModal, setSuggestionType} from "../../../../../../store/ui/actions";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons.jsx';
import {siteDomain} from '../../../../../../Utils/domains'


class Experience extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteExperience = this.deleteExperience.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],
            fieldArray: [],
            length:0,
            currentIndex: null,
            modal_status:false

        };
        this.props.currentForm('experience');
    }

    componentDidMount() {

        this.props.fetchUserExperience();
        let till_today = [];
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_working)
        }
        this.setState({till_today})
    }

    async componentDidUpdate(prevProps) {
        const {ui:{previewClicked},previewButtonClicked,history,initialValues} = this.props;
        if(previewClicked !== prevProps.ui.previewClicked && previewClicked){
            await this.updateInfoBeforeLoss()
            this.setState({submit:true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
        if (initialValues.list !== prevProps.initialValues.list) {
            let till_today = [];
            for (let i of initialValues.list) {
                till_today.push(i.is_working)
            }
            this.setState({till_today})
        }
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()

    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state;
        till_today[parseInt(index)] = checked
    }

    async handleSubmit(values, entityLink, currentFields) {
         const {userInfo:{order_data},hideGenerateResumeModal,showGenerateResumeModal,history,reGeneratePDF} = this.props
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else if(order_data && order_data.id){
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

    }

    async updateInfoBeforeLoss(){
        let { initialValues, formData: {experience: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues)!==JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
    }

    async openModal(fields,index){

        const {job_profile:{label},work_description} = fields.get(index)
        this.setState({length:work_description.length})
        await this.props.fetchJobTitles(label || '','experience')
        this.setState({modal_status:true,scrollpos:window.scrollY,fields,currentIndex:index})
    }

    closeModal(suggestions){
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

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "job_profile": {
                "label": '',
                "value": ''
            },
            "company_name": '',
            "start_date": '',
            "end_date": '',
            "is_working": false,
            "job_location": '',
            "work_description": '',
            order: listLength
        })

        scroller.scrollTo(`experience${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 470,
            containerId: 'experience'
        })
    }

    deleteExperience(index, fields, event) {
        event.stopPropagation();
        const experience = fields.get(index);
        fields.remove(index);
        if (experience && experience.id) {
            this.props.removeExperience(experience.id)
        }
    }


    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit,userInfo:{order_data}, ui: {loader,suggestions}, isEditable,
            editHeading, saveTitle, entityName, nextEntity, showAlertModal,history,
            changeOrderingDown, changeOrderingUp, handleInputValue, currentFields, fetchJobTitles
        } = this.props;
        const {till_today,modal_status,length} = this.state;

        return (
            <React.Fragment>
                <SuggestionModal label={'Job Description'} modal_status={modal_status} maxLength="300" length={length} closeModal={this.closeModal} suggestions={suggestions}/>
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity, currentFields))}>
                    <FieldArray name={"list"}
                                loader={loader}
                                handleSubmit={handleSubmit}
                                handleAccordionClick={this.handleAccordionClick}
                                handleAddition={this.handleAddition}
                                deleteExperience={this.deleteExperience}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                component={ExperienceRenderer}
                                saveTitle={(event) => saveTitle(event, 3)}
                                editHeading={(value) => editHeading(value)}
                                isEditable={isEditable}
                                entityName={entityName}
                                expanded={this.state.active}
                                fetchJobTitles={(inputValue) => fetchJobTitles(inputValue, '')}
                                till_today={till_today}
                                tillTodayDisable={this.tillTodayDisable}
                                handleInputValue={handleInputValue}
                                openModal={this.openModal}
                                


                    />

                    <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                    />
                </form>
            </React.Fragment>
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
        ui: state.ui,
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

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userExperience, index) => {
                const {start_date, end_date, job_profile} = userExperience;
                if (!userExperience['id']) delete userExperience['id'];
                userExperience = {
                    ...userExperience,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
                        order: index,
                        job_profile: job_profile && job_profile.value || ''
                    }
                };
                return userExperience;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserExperience({list: listItems, resolve, reject}))
            })

        },
        "fetchJobTitles": (inputValue, suggestionType) => {
            if (inputValue.length < 3) return new Promise(res => res([]));
            return new Promise((res, rej) => {
                return dispatch(actions.fetchJobTitles({inputValue, suggestionType, res, rej}))
            })
        },
        "hideSuggestionModal": () => {
            return dispatch(hideSuggestionModal())
        },
        "showSuggestionModal": () => {
            return dispatch(showSuggestionModal())
        },
        "setSuggestionType": (type) => {
            return dispatch(setSuggestionType(type))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
