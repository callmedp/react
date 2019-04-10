import React, {Component} from 'react';
import './education.scss'
import {Field, reduxForm} from "redux-form";
import {renderField, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'

import * as actions from "../../../../../../store/education/actions";
import {connect} from "react-redux";
import moment from "moment";


class Education extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=skill')
    }

    componentDidMount() {
        this.props.fetchUserEducation()
    }

    render() {
        const {handleSubmit, education} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-education1"></i></span>
                    <h2>Education</h2>
                    <span className="icon-edit icon-education__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{education.specialization}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Institution Name </label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-company"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="institution_name"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Specialization</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-company"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="specialization"/>
                                    </div>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Date from</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} type={"date"} name="start_date"
                                               className="input-control"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Date to</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} type={"date"} name="end_date"
                                               className="input-control"/>

                                    </div>
                                    <span className="till-today">
                                    <Field type="radio" name="is_pursuing" component={'input'}
                                           value={education.is_pursuing}/>
                                    Till Today
                                </span>
                                </fieldset>
                            </div>

                            <div className="flex-container">

                                <fieldset className="custom">
                                    <label>Course Type</label>
                                    <Field component={renderSelect} type={"text"} name="course_type"
                                           options={[
                                               {value: 'FT', label: 'FULL TIME'},
                                               {value: 'PT', label: 'PART TIME'},
                                           ]}
                                           className="input-control"/>
                                </fieldset>
                                <fieldset>
                                    <label>Percentage/CGPA</label>
                                    <Field component={renderField} type={"text"} name="percentage_cgpa"
                                           className="input-control"/>
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


export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education,
        education: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userEducation) => {
            const {start_date, end_date, course_type} = userEducation;

            userEducation = {
                ...userEducation,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                    course_type: course_type && course_type.value
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserEducation({userEducation, resolve, reject}));
            })
        },
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
