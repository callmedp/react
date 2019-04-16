import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {required} from "../../../../../FormHandler/formValidations"
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
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Education</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    <form onSubmit={handleSubmit(this.handleSubmit)}>
                        <div className="subHeading pb-0">
                            <h2>{education.specialization}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" role="button"></span>
                                </li>
                                <li className="subHeading__btn">
                                    <i className="sprite icon--upArrow"></i>
                                </li>
                                <li className="subHeading__btn">
                                    <i className="sprite icon--downArrow"></i>
                                </li>
                            </ul>
                        </div>

                        <ul className="form pb-0">
                            <li className="form__group">
                                <label className="form__label" for="institution_name">Institution Name </label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--education-grey"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} validate={required}
                                     name="institution_name" className="form__input" id="institution_name" aria-label="institution_name"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="specialization">Specialization</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} validate={required}
                                     name="specialization" className="form__input" id="specialization" aria-label="specialization"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="start_date">Date from</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={datepicker} type={"date"} validate={required} name="start_date"
                                      aria-label="start_date" id="start_date" className="form__input"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="end_date">Date to</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={datepicker} type={"date"} validate={required} name="end_date"
                                      aria-label="end_date" id="end_date" className="form__input"/>
                                </div>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <input class="form__radio-input" type="radio" name="tillToday" id="tillToday" value="option2" />
                                <label class="form__radio-label" for="tillToday">
                                    <span className="form__radio-button"></span>
                                    Till today
                            </label>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="course_type">Course Type</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderSelect} validate={required} type={"text"} name="course_type"
                                           options={[
                                               {value: 'FT', label: 'FULL TIME'},
                                               {value: 'PT', label: 'PART TIME'},
                                           ]}
                                           className="form__input" validate={required} id="course_type" 
                                           aria-label="course_type"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="percentage_cgpa">Percentage/CGPA</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} validate={required}
                                     name="percentage_cgpa" className="form__input" id="percentage_cgpa" aria-label="percentage_cgpa"/>
                                </div>
                            </li>

                        </ul>

                        <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary" type={'submit'}>Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                    </form>
                </div>
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
