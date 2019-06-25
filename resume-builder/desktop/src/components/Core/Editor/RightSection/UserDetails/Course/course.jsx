import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import validate from "../../../../../FormHandler/validations/course/validate"
import moment from "moment";
import {CourseRenderer} from "./courseRenderer";
import {scroller} from "react-scroll/modules";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import {siteDomain} from '../../../../../../Utils/domains'

class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteCourse = this.deleteCourse.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false

        }
        this.props.currentForm('course');
    }

    componentDidMount() {

        this.props.fetchUserCourse()
    }

    async handleSubmit(values, entityLink) {
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
            }, 5000);
        }
        else{
            history.push(`/resume-builder/buy`) 
        }
        }

    }

    async componentDidUpdate(prevProps) {
        const {ui: {previewClicked}, previewButtonClicked, history} = this.props;
        if (previewClicked !== prevProps.ui.previewClicked && previewClicked) {
            await this.updateInfoBeforeLoss()
            this.setState({submit: true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }

    async updateInfoBeforeLoss(){
        let { initialValues, formData: {course: {values, syncErrors}}} = this.props;
        let error = false;
        ((syncErrors && syncErrors['list']) || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) await this.props.bulkUpdateOrCreate(values && values['list'])
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "name_of_certification": '',
            "year_of_certification": '',
            order: listLength
        })

        scroller.scrollTo(`course${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 200,
            containerId: 'course'
        })
    }

    deleteCourse(index, fields, event) {
        event.stopPropagation();
        const course = fields.get(index);
        fields.remove(index);
        if (course && course.id) {
            this.props.removeCourse(course.id)
        }
    }

    handleAccordionClick(value) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit,userInfo:{order_data}, ui: {loader}, editHeading, saveTitle, isEditable,
            entityName, nextEntity, showAlertModal,history, handleInputValue, changeOrderingUp, changeOrderingDown
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={'list'}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteCourse={this.deleteCourse}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={CourseRenderer}
                            saveTitle={(event) => saveTitle(event, 8)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                            expanded={this.state.active}
                            handleInputValue={handleInputValue}
                />
                <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                    />
            </form>

        )
    }
}


export const
    CourseForm = reduxForm({
        form: 'course',
        enableReinitialize: true,
        onSubmitFail: (errors) => scrollOnErrors(errors, 'course', -100),
        validate
    })(Course);


const
    mapStateToProps = (state) => {
        return {
            initialValues: state.course,
            ui: state.ui
        }
    };

const
    mapDispatchToProps = (dispatch) => {
        return {
            "onSubmit": (userCourse) => {
                const {year_of_certification} = userCourse;
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                    }
                };
                return new Promise((resolve, reject) => {
                    return dispatch(actions.updateUserCourse({userCourse, resolve, reject}));
                })
            },
            "fetchUserCourse": () => {
                return dispatch(actions.fetchUserCourse())
            },
            "removeCourse": (courseId) => {
                return dispatch(actions.deleteCourse(courseId))
            },

            "bulkUpdateOrCreate": (listItems) => {
                listItems = (listItems || []).map((userCourse, index) => {
                    const {year_of_certification} = userCourse;
                    if (!userCourse['id']) delete userCourse['id'];
                    userCourse = {
                        ...userCourse,
                        ...{
                            year_of_certification: (year_of_certification && year_of_certification.value && Number(year_of_certification.value)) || null,
                            order: index
                        }
                    };
                    return userCourse;
                });
                return new Promise((resolve, reject) => {
                    return dispatch(actions.bulkUpdateOrCreateUserCourse({list: listItems, resolve, reject}))
                })

            },
        }
    };

export default connect(mapStateToProps, mapDispatchToProps)(CourseForm)
;
