import React, {Component} from 'react';
import './experience.scss'
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions';
import {connect} from "react-redux";
import moment from 'moment';
import {required} from "../../../../../FormHandler/formValidations"

class Experience extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);

    }
    componentDidMount() {
        this.props.fetchUserExperience()
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=education')
    }

    render() {
        const {handleSubmit, experience} = this.props;
        return (
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Experience</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    <form onSubmit={handleSubmit(this.handleSubmit)}>
                        <div className="subHeading pb-0">
                            <h2>{experience.company_name}</h2>
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
                                <label className="form__label" for="job_profile">Designation</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--designation"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} 
                                    name="job_profile" aria-label="job_profile" id="job_profile" className="form__input"  />
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="company_name">Company name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--company"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} 
                                      name="company_name" aria-label="company_name" id="company_name" className="form__input"/>
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
                                    <Field component={datepicker} validate={required} type={"date"} 
                                    className="form__input" name="start_date" aria-label="start_date" id="start_date"/>
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
                                    <Field component={datepicker} validate={required} type={"date"} 
                                    className="form__input" name="end_date" aria-label="end_date" id="end_date"/>
                                </div>
                            </li>


                            
                            <li className="form__group">
                                <label className="form__label" for="job_location">Job Location</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--company"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} name="job_location"
                                        id="job_location" className="form__input"/>
                                </div>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <Field type="radio" name="is_working" component="input" className="form__radio-input"
                                    id="is_working"  value={experience.is_working}/>
                                <label class="form__radio-label" for="is_working">
                                    <span className="form__radio-button"></span>
                                    Till today
                            </label>
                            </li>
                        </ul>

                        <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary">Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                    </form>
                </div>
            </div>
        )
    }
}

export const ExperienceForm = reduxForm({
    form: 'experience',
    enableReinitialize: true
})(Experience);


const mapStateToProps = (state) => {
    return {
        initialValues: state.experience,
        experience: state.experience
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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
