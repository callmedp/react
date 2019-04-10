import React, {Component} from 'react';
import './experience.scss'
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions/index';
import {connect} from "react-redux";
import moment from 'moment';

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
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-experience1"></i></span>
                    <h2>Experience</h2>
                    <span className="icon-edit icon-experience__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{experience.company_name}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>Designation</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-designation"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="job_profile"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Company Name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-company"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="company_name"/>
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
                                        <Field component={datepicker} type={"date"} className={'input-control'}
                                               name="start_date"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Date to</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} type={"date"} name="end_date"
                                               className={'input-control'}/>
                                    </div>
                                    <span className="till-today">
									<Field type="radio" name="is_working" component="input"
                                           value={experience.is_working}/>
									Till Today
								</span>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Job Location</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-address"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="job_location"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Description</label>
                                    <Field component={renderTextArea} rows={"3"} type={"text"} name="work_description"/>
                                </fieldset>
                            </div>

                        </section>


                    </section>

                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type="submit">Save & Continue</button>
                    </div>
                </form>

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
