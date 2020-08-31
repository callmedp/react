import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import validate from "../../../../../FormHandler/validtaions/education/validate";
import * as actions from "../../../../../../store/education/actions";
import { connect } from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderEducation from "./renderEducation"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';
import propTypes from 'prop-types';

class Education extends Component {
    
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteEducation = this.deleteEducation.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false,
            'till_today': [],
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
    }
    
    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserEducation, updateCurrentLinkPos, history,
        generateResumeAlert } = this.props
        currentLinkPos++
        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            
            values.map(el => {
                if (!el.institution_name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserEducation(values);
            }
        }
        this.setState({ submit: true })
        if (currentLinkPos === listOfLinks.length) {
            currentLinkPos = 0
            generateResumeAlert()
        }
        else {
            updateCurrentLinkPos({ currentLinkPos })
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
        
    }
    
    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let { till_today } = this.state
        till_today[parseInt(index)] = checked
    }
    
    async updateInfoBeforeLoss() {
        
        if (!this.state.submit) {
            const { initialValues } = this.props
            
            const form_data = this.props.info.form.education;
            let error = false
            let error_values = form_data["syncErrors"]
            if (error_values) {
                for (let i of error_values['list']) {
                    for (let j of Object.keys(i)) {
                        if (i[j]) {
                            error = true
                            break;
                        }
                    }
                }
            }
            if (!error && JSON.stringify(initialValues) !== JSON.stringify(form_data['values'])) {
                
                const values = this.props.handleOrdering(form_data['values'])
                await this.props.bulkUpdateUserEducation(values.list)
            }
        }
    }
    
    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }
    
    editHeadingClick() {
        this.setState({ editHeading: true })
        this.props.sendTrackingInfo('right_section_edit',1)
    }
    
    
    componentDidMount() {
        this.props.fetchUserEducation()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_pursuing)
        }
        this.setState({ till_today })
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[1].entity_text })
        }
    }
    
    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[1].entity_text })
        }
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.is_pursuing)
            }
            this.setState({ till_today })
        }
    }
    
    deleteEducation(index, fields, event) {
        this.props.sendTrackingInfo('right_section_delete',1)
        event.stopPropagation();
        const education = fields.get(index);
        fields.remove(index);
        if (education && education.id) {
            
            this.props.removeEducation(education.id)
        }
    }
    
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { updateAlertModalStatus, handleSubmit, submitting, personalInfo: { order_data, entity_preference_data }, 
        headingChange, history, changeOrderingUp, changeOrderingDown, eventClicked , showAlertMessage
    } = this.props;
        const { editHeading, heading, till_today } = this.state;
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props} />
                    <Subscribe {...this.props} />
                    <FieldArray name={'list'}
                        sendTrackingInfo = {this.props.sendTrackingInfo}
                        handleSubmit={handleSubmit}
                        handleAddition={this.props.handleAddition}
                        deleteEducation={this.deleteEducation}
                        changeOrderingUp={changeOrderingUp}
                        changeOrderingDown={changeOrderingDown}
                        eventClicked={eventClicked}
                        component={renderEducation}
                        headingChange={headingChange}
                        entity_preference_data={entity_preference_data}
                        editHeading={editHeading}
                        editHeadingClick={this.editHeadingClick}
                        heading={heading}
                        context={this}
                        till_today={till_today}
                        tillTodayDisable={this.tillTodayDisable}
                        showAlertMessage={showAlertMessage}
                         />
                    <ul className="form">
                        <li className="form__group">
                            <BottomCTC disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
                                length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                                order_data={order_data} eventClicked={eventClicked} form_name={'Education'} />
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

Education.propTypes = {
    bulkUpdateUserEducation: propTypes.func,
    changeOrderingDown: propTypes.func,
    changeOrderingUp: propTypes.func,
    education: propTypes.shape({
        list: propTypes.array
    }),
    eventClicked: propTypes.func,
    fetchUserEducation: propTypes.func,
    generateResumeAlert: propTypes.func,             
    handleAddition: propTypes.func,
    handleOrdering: propTypes.func,
    handleSubmit: propTypes.func,
    headingChange: propTypes.func,             
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
        currentLinkPos: propTypes.string,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
    personalInfo: propTypes.shape({
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        gender: propTypes.string,
        hide_subscribe_button: propTypes.bool,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
    }),
    removeEducation: propTypes.func,
    showAlertMessage: propTypes.func,
    sidenav: propTypes.shape({
        currentLinkPos: propTypes.string,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    submitting: propTypes.bool,
    updateAlertModalStatus: propTypes.func,
    updateCurrentLinkPos: propTypes.func,
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
        education: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
        "removeEducation": (educationId) => {
            return dispatch(actions.deleteEducation(educationId))
        },
        
        "bulkUpdateUserEducation": (listItems) => {
            listItems = (listItems || []).map(userEducation => {
                const { start_date, end_date, course_type } = userEducation;
                if (!userEducation['id']) delete userEducation['id'];
                userEducation = {
                    ...userEducation,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
                    }
                };
                return userEducation;
            }
            );
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserEducation({ list: listItems, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
