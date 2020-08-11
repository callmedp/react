import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/education/actions";
import { connect } from "react-redux";
import moment from "moment";
import { EducationRenderer } from "./educationRenderer";
import validate from '../../../../../FormHandler/validations/education/validate';
import { scroller } from "react-scroll/modules";
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import propTypes from 'prop-types';

class Education extends Component {
    static propTypes = {
        currentForm: propTypes.func,
        generateResumeAlert: propTypes.func,
        bulkUpdateOrCreate: propTypes.func,
        eventClicked: propTypes.func,
        history: propTypes.shape({
            action: propTypes.string,
            block: propTypes.func,
            createHref: propTypes.func,
            go: propTypes.func,
            goBack: propTypes.func,
            goForward: propTypes.func,
            length: propTypes.number,
            listen: propTypes.func,
            location: propTypes.shape({
                hash: propTypes.string,
                pathname: propTypes.string,
                search: propTypes.string,
                state: undefined
            }),
            push: propTypes.func,
            replace: propTypes.func, 
        }),
        initialValues: propTypes.shape({
            list: propTypes.array
        }),
        fetchUserEducation: propTypes.func,
        ui: propTypes.shape({
            alertModal: propTypes.bool,
            formName: propTypes.string,
            generateResumeModal: propTypes.bool,
            helpModal: propTypes.bool,
            loader: propTypes.bool,
            loginModal: propTypes.bool,
            modal: propTypes.bool,
            previewClicked: propTypes.bool,
            select_template_modal: propTypes.bool,
            showMoreSection: propTypes.bool,
            successLogin: propTypes.bool,
            suggestionModal: propTypes.bool,
            suggestionType: propTypes.string,
            suggestions: propTypes.array,
        }),
        previewButtonClicked: propTypes.func,
        formData: propTypes.object,
        removeEducation: propTypes.func,
        handleSubmit: propTypes.func,
        saveTitle: propTypes.func,
        editHeading: propTypes.func,
        isEditable: propTypes.bool,
        entityName: propTypes.string,
        handleInputValue: propTypes.func,
        showAlertModal: propTypes.func,
        changeOrderingDown: propTypes.func,
        changeOrderingUp: propTypes.func,
        showAlertMessage: propTypes.func,
        userInfo: propTypes.shape({
            active_subscription: propTypes.bool,
            candidate_id: propTypes.string,
            date_of_birth: propTypes.string,
            email: propTypes.string,
            entity_preference_data: propTypes.array,
            extra_info: propTypes.string,
            extracurricular: propTypes.array,
            first_name: propTypes.string,
            free_resume_downloads: propTypes.number,
            gender: propTypes.object,
            id: propTypes.number,
            image: propTypes.string,
            interest_list: propTypes.array,
            last_name: propTypes.string,
            location: propTypes.string,
            number: propTypes.string,
            selected_template: propTypes.string,
        }),
    }
    
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteEducation = this.deleteEducation.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],
        }
        this.props.currentForm('education');
        console.log(this.props);
    }
    
    async handleSubmit(values, entityLink) {
        const { generateResumeAlert, bulkUpdateOrCreate, history } = this.props
        const { list } = values;
        if (list.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            list.map(el => {
                if (!el.institution_name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateOrCreate(list);
            }
            
        }
        
        this.setState({
            submit: true
        })
        
        if (entityLink) history.push(entityLink);
        else {
            generateResumeAlert()
        }
        
    }
    
    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }
    
    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let { till_today } = this.state
        till_today[parseInt(index)] = checked
    }
    
    componentDidMount() {
        
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_pursuing)
        }
        this.setState({ till_today })
        this.props.fetchUserEducation()
    }
    
    async componentDidUpdate(prevProps) {
        const { ui: { previewClicked }, previewButtonClicked, history, initialValues } = this.props;
        if (previewClicked !== prevProps.ui.previewClicked && previewClicked) {
            await this.updateInfoBeforeLoss()
            this.setState({ submit: true })
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
        if (initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of initialValues.list) {
                till_today.push(i.is_pursuing)
            }
            this.setState({ till_today })
        }
    }
    
    async updateInfoBeforeLoss() {
        let { initialValues, formData: { education: { values, syncErrors }}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues) !== JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
    }
    
    
    
    handleAddition(fields, error, event) {
        const listLength = fields.length;
        fields.push({
            "candidate_id": '',
            "id": '',
            "specialization": '',
            "institution_name": '',
            "course_type": '',
            "start_date": '',
            "percentage_cgpa": '',
            "end_date": '',
            "is_pursuing": false,
            order: listLength
        })
        
        scroller.scrollTo(`education${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 350,
            containerId: 'education'
        })
        this.props.eventClicked({
            'action': 'AddNew',
            'label': 'Education'
        })
        
    }
    
    deleteEducation(index, fields, event) {
        event.stopPropagation();
        const education = fields.get(index);
        fields.remove(index);
        if (education && education.id) {
            this.props.removeEducation(education.id)
        }
    }
    
    handleAccordionClick(value, fields) {
        this.setState({ active: value })
    }
    
    render() {
        const {
            handleSubmit, userInfo: { order_data }, ui: { loader }, saveTitle, isEditable, eventClicked,
            editHeading, entityName, nextEntity, handleInputValue, showAlertModal, history, changeOrderingUp
            , changeOrderingDown, showAlertMessage
        } = this.props;
        const { till_today } = this.state
        
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
            <FieldArray name={'list'}
            loader={loader}
            handleSubmit={handleSubmit}
            handleAccordionClick={this.handleAccordionClick}
            handleAddition={this.handleAddition}
            deleteEducation={this.deleteEducation}
            changeOrderingUp={changeOrderingUp}
            changeOrderingDown={changeOrderingDown}
            component={EducationRenderer}
            saveTitle={(event) => saveTitle(event, 2)}
            editHeading={() => editHeading(2)}
            isEditable={isEditable}
            entityName={entityName}
            expanded={this.state.active}
            till_today={till_today}
            tillTodayDisable={this.tillTodayDisable}
            handleInputValue={handleInputValue}
            showAlertMessage={showAlertMessage}
            />
            
            <SavePreviewButtons
            showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'Education'}
            nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
            />
            
            </form>
            )
        }
    }
    
    
    export const EducationForm = reduxForm({
        form: 'education',
        enableReinitialize: true,
        onSubmitFail: (errors) => scrollOnErrors(errors, 'education', -100),
        validate
    })(Education);
    
    
    const mapStateToProps = (state) => {
        return {
            initialValues: state.education,
            ui: state.ui,
        }
    };
    
    const mapDispatchToProps = (dispatch) => {
        return {
            "onSubmit": (userEducation) => {
                const { start_date, end_date, course_type } = userEducation;
                
                userEducation = {
                    ...userEducation,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
                        course_type: course_type && course_type.value
                    }
                };
                return new Promise((resolve, reject) => {
                    return dispatch(actions.updateUserEducation({ userEducation, resolve, reject }));
                })
            },
            "fetchUserEducation": () => {
                return dispatch(actions.fetchUserEducation())
            },
            "removeEducation": (educationId) => {
                return dispatch(actions.deleteEducation(educationId))
            },
            
            "bulkUpdateOrCreate": (listItems) => {
                listItems = (listItems || []).map((userEducation, index) => {
                    const { start_date, end_date, course_type } = userEducation;
                    if (!userEducation['id']) delete userEducation['id'];
                    userEducation = {
                        ...userEducation,
                        ...{
                            start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                            end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
                            course_type: course_type && course_type.value,
                            order: index
                        }
                    };
                    return userEducation;
                }
                );
                return new Promise((resolve, reject) => {
                    return dispatch(actions.bulkUpdateOrCreateUserEducation({ list: listItems, resolve, reject }))
                })
                
            },
            
        }
        
    };
    
    export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
    