import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import { connect } from "react-redux";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderCourse from "./renderCourse";
import validate from "../../../../../FormHandler/validtaions/course/validate"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';
import propTypes from 'prop-types';

class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteCourse = this.deleteCourse.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
    }
    
    componentDidMount() {
        this.props.fetchUserCourse()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[7].entity_text })
        }
    }
    
    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserCourse, generateResumeAlert, updateCurrentLinkPos,
        history } = this.props
        currentLinkPos++
        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            
            values.map(el => {
                if (!el.name_of_certification) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserCourse(values);
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
    
    deleteCourse(index, fields, event) {
        event.stopPropagation();
        const course = fields.get(index);
        fields.remove(index);
        if (course && course.id) {
            this.props.removeCourse(course.id)
        }
    }
    
    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[7].entity_text })
        }
    }
    
    async updateInfoBeforeLoss() {
        
        if (!this.state.submit) {
            const { initialValues } = this.props
            const form_data = this.props.info.form.course;
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
                await this.props.bulkUpdateUserCourse(values.list)
            }
        }
    }
    
    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }
    
    editHeadingClick() {
        this.setState({ editHeading: true })
    }
    
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { updateAlertModalStatus, handleSubmit, history, submitting, personalInfo: { order_data, entity_preference_data }, headingChange, changeOrderingUp, changeOrderingDown, eventClicked, showAlertMessage } = this.props;
        const { editHeading, heading } = this.state;
        return (
            
            <div className="buildResume">
            <PreviewModal {...this.props} />
            <Subscribe {...this.props} />
            <form onSubmit={handleSubmit(this.handleSubmit)}>
            <FieldArray name="list"
            handleSubmit={handleSubmit}
            handleAddition={this.props.handleAddition}
            deleteCourse={this.deleteCourse}
            changeOrderingUp={changeOrderingUp}
            changeOrderingDown={changeOrderingDown}
            eventClicked={eventClicked}
            component={renderCourse}
            headingChange={headingChange}
            entity_preference_data={entity_preference_data}
            editHeading={editHeading}
            editHeadingClick={this.editHeadingClick}
            context={this}
            heading={heading}
            showAlertMessage={showAlertMessage}
            />
            <ul className="form">
            <li className="form__group">
            <BottomCTC disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
            length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
            order_data={order_data} eventClicked={eventClicked} form_name={'Courses'} />
            </li>
            </ul>
            </form>
            </div>
            )
        }
    }
    
    Course.propTypes = {
        bulkUpdateUserCourse: propTypes.func,
        changeOrderingDown: propTypes.func,
        changeOrderingUp: propTypes.func,
        eventClicked: propTypes.func,
        fetchUserCourse: propTypes.func,
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
        removeCourse: propTypes.func,
        sidenav: propTypes.shape({
            currentLinkPos: propTypes.string,
            listOfLinks: propTypes.array,
            sidenavStatus: propTypes.bool
        }),
        submitting: propTypes.bool,
        updateAlertModalStatus: propTypes.func,
        updateCurrentLinkPos: propTypes.func,
    }
    
    export const CourseForm = reduxForm({
        form: 'course',
        enableReinitialize: true,
        onSubmitFail: (errors) => scrollOnErrors(errors, 'course', -100),
        validate
    })(Course);
    
    
    const mapStateToProps = (state) => {
        return {
            initialValues: state.course,
            course: state.course
        }
    };
    
    const mapDispatchToProps = (dispatch) => {
        return {
            "onSubmit": (userCourse) => {
                const { year_of_certification } = userCourse;
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: parseInt(year_of_certification)
                    }
                };
                return new Promise((resolve, reject) => {
                    return dispatch(actions.updateUserCourse({ userCourse, resolve, reject }));
                })
            },
            "fetchUserCourse": () => {
                return dispatch(actions.fetchUserCourse())
            },
            "removeCourse": (courseId) => {
                return dispatch(actions.deleteCourse(courseId))
            },
            
            "bulkUpdateUserCourse": (listItems) => {
                listItems = (listItems || []).map(userCourse => {
                    const { year_of_certification } = userCourse;
                    if (!userCourse['id']) delete userCourse['id'];
                    userCourse = {
                        ...userCourse,
                        ...{
                            year_of_certification: parseInt(year_of_certification)
                        }
                    };
                    return userCourse;
                })
                return new Promise((resolve, reject) => {
                    return dispatch(actions.bulkUpdateUserCourse({ list: listItems, resolve, reject }))
                })
            }
        }
    };
    
    export default connect(mapStateToProps, mapDispatchToProps)(CourseForm);
    