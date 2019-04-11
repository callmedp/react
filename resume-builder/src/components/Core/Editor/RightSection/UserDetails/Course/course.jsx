import React, {Component} from 'react';
import './course.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"
import moment from "moment";


class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserCourse()
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=project')
    }

    render() {
        const {handleSubmit, course} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-courses1"></i></span>
                    <h2>Courses</h2>
                    <span className="icon-edit icon-courses__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{course.name_of_certification}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Course Name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-courses-gr"></span>
                                        </div>
                                        <Field component={renderField} validate={required} type={"text"} name="name_of_certification" className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Completion Year</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} validate={required} type={"date"} name="year_of_certification"
                                               className="input-control"/>

                                    </div>
                                </fieldset>
                            </div>

                        </section>


                    </section>

                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>

            </div>
        )
    }
}


export const CourseForm = reduxForm({
    form: 'course',
    enableReinitialize: true
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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CourseForm);
