import React, {Component} from 'react';
import './course.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../store/course/actions";
import {connect} from "react-redux";
import {renderField} from "../../../../FormHandler/formFieldRenderer.jsx";


class Course extends Component {

    componentDidMount() {
        this.props.fetchUserCourse()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-courses1"></i></span>
                    <h2>Courses</h2>
                    <span className="icon-edit icon-courses__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Course 1</h3>
                            <div className="addon-buttons mr-10">
                                <span className="icon-delete mr-15"></span>
                                <span className="icon-ascend mr-5"></span>
                                <span className="icon-descend"></span>
                            </div>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>Course Name</label>
                                <Field component={renderField} type={"text"} name="name_of_certification"/>
                            </fieldset>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>Date from</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <input type="text" placeholder="" className="input-control"/>
                                </div>
                            </fieldset>
                            <fieldset>
                                <label>Date to</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <input type="text" placeholder="" className="input-control"/>
                                </div>
                                <span className="till-today">
									<input type="radio" name="" checked/>
									Till Today
								</span>
                            </fieldset>
                        </div>

                    </section>


                </section>

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button">Save & Continue</button>
                </div>

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
        initialValues: state.course
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserCourse": () => {
            return dispatch(actions.fetchUserCourse())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CourseForm);
