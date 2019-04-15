import React, {Component} from 'react';
import './course.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";
import validate from "../../../../../FormHandler/validations/courseValidation"
import moment from "moment";

import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';


class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteCourse = this.deleteCourse.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,

        }
    }

    componentDidMount() {
        this.props.fetchUserCourse()
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=project')
    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        console.log('donw pressed');
        fields.swap(index, index + 1);
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('up pressed');
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "name_of_certification": '',
            "year_of_certification": '',
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


    handleAccordionState(val, fields) {
        const {currentAccordion} = this.state;

        console.log('--accordion--', currentAccordion);
        if (currentAccordion !== '') {

            this.props.onSubmit(fields.get(currentAccordion))
        }

        this.setState((state) => ({
            previousAccordion: state.currentAccordion,
            openedAccordion: val,
            currentAccordion: val
        }))
    }

    handleAccordionClick(value, fields) {
        const val = value.length > 0 ? value[0] : ''
        this.handleAccordionState(val, fields)
    }

    render() {
        const {handleSubmit, course} = this.props;
        const renderCourse = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                <div>
                    <section className="head-section">
                        <span className="icon-box"><i className="icon-courses1"></i></span>
                        <h2>Courses</h2>
                        <span className="icon-edit icon-courses__cursor"></span>
                        <button onClick={this.handleAddition.bind(this, fields, error)}
                                type={'button'}
                                className="add-button add-button__right">Add new
                        </button>
                        {(touched || submitFailed) && error && <span>{error}</span>}
                    </section>
                    <section className="right-sidebar-scroll">
                        <ul>
                            <Accordion
                                onChange={(value) => this.handleAccordionClick(value, fields, error)}
                                allowZeroExpanded={true}
                                preExpanded={[this.state.openedAccordion]}
                            >
                                {
                                    fields.map((member, index) => {
                                        return (
                                            <li key={index}>
                                                <section className="info-section">
                                                    <AccordionItem uuid={index}>
                                                        <AccordionItemHeading>
                                                            <AccordionItemButton>
                                                                <div className="flex-container">
                                                                    <h3 className="add-section-heading">{fields.get(index).name_of_certification || 'Course'}</h3>
                                                                    <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => this.deleteCourse(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                        {index !== 0 &&
                                                                        <span
                                                                            onClick={(event) => this.changeOrderingUp(index, fields, event)}
                                                                            className="icon-ascend mr-5"/>
                                                                        }
                                                                        {
                                                                            index !== fields.length - 1 &&
                                                                            < span
                                                                                onClick={(event) => this.changeOrderingDown(index, fields, event)}
                                                                                className="icon-descend"/>
                                                                        }
                                                                    </div>
                                                                </div>
                                                            </AccordionItemButton>
                                                        </AccordionItemHeading>
                                                        <AccordionItemPanel>
                                                            <div className="flex-container">
                                                                <fieldset>
                                                                    <label>Course Name</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-courses-gr"></span>
                                                                        </div>
                                                                        <Field component={renderField}
                                                                               type={"text"}
                                                                               name={`${member}.name_of_certification`}
                                                                               className={"input-control"}/>
                                                                    </div>
                                                                </fieldset>
                                                                <fieldset>
                                                                    <label>Completion Year</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-date"></span>
                                                                        </div>
                                                                        <Field component={datepicker}
                                                                               type={"date"}
                                                                               name={`${member}.year_of_certification`}
                                                                               className="input-control"/>
                                                                    </div>
                                                                </fieldset>
                                                            </div>
                                                        </AccordionItemPanel>
                                                    </AccordionItem>
                                                </section>
                                            </li>
                                        )
                                    })
                                }
                            </Accordion>
                        </ul>
                    </section>
                </div>
            );
        }

        return (
            <div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name={'list'} component={renderCourse}/>
                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>
            </div>
        )
    }
}


export const
    CourseForm = reduxForm({
        form: 'course',
        enableReinitialize: true,
        validate
    })(Course);


const
    mapStateToProps = (state) => {
        return {
            initialValues: state.course,
            course: state.course
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

            "handleSwap": (listItems) => {
                return dispatch(actions.handleCourseSwap({list: listItems}))
            }
        }
    };

export default connect(mapStateToProps, mapDispatchToProps)

(
    CourseForm
)
;
