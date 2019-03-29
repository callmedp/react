import React, {Component} from 'react';
import './experience.scss'
import {renderField, renderTextArea} from '../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm} from 'redux-form';
import * as actions from '../../../../../store/experience/actions/index';
import {connect} from "react-redux";


class Experience extends Component {

    componentDidMount() {
        this.props.fetchUserExperience()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-experience1"></i></span>
                    <h2>Experience</h2>
                    <span className="icon-edit icon-experience__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Company1</h3>
                            <div className="addon-buttons mr-10">
                                <span className="icon-delete mr-15"></span>
                                <span className="icon-ascend mr-5"></span>
                                <span className="icon-descend"></span>
                            </div>
                        </div>
                        <div className="flex-container">
                            <fieldset className="error">
                                <label>Designation</label>
                                <Field component={renderField} type={"text"} name="job_profile"/>

                            </fieldset>
                            <fieldset>
                                <label>Company Name</label>
                                <Field component={renderField} type={"text"} name="company_name"/>
                            </fieldset>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>Date from</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <Field component={renderField} type={"text"} className={'input-control'}
                                           name="start_date"/>
                                </div>
                            </fieldset>
                            <fieldset>
                                <label>Date to</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <Field component={renderField} type={"text"} name="end_date"
                                           className={'input-control'}/>
                                </div>
                                <span className="till-today">
									<input type="radio" name="" checked/>
									Till Today
								</span>
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
                    <button className="orange-button">Save & Continue</button>
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
        initialValues: state.experience
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserExperience": () => {
            return dispatch(actions.fetchUserExperience())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
