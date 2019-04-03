import React, {Component} from 'react';
import './education.scss'
import {Field, reduxForm} from "redux-form";
import {renderField, renderTextArea} from '../../../../FormHandler/formFieldRenderer.jsx'

import * as actions from "../../../../../store/education/actions";
import {connect} from "react-redux";


class Education extends Component {
    constructor(props){
        super(props);
    }

    componentDidMount() {
        this.props.fetchUserEducation()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-education1"></i></span>
                    <h2>Education</h2>
                    <span className="icon-edit icon-education__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Education1</h3>
                            <div className="addon-buttons mr-10">
                                <span className="icon-delete mr-15"></span>
                                <span className="icon-ascend mr-5"></span>
                                <span className="icon-descend"></span>
                            </div>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>School name, degree </label>
                                <Field component={renderField} type={"text"} name="institution_name"/>
                            </fieldset>
                            <fieldset>
                                <label>Date from</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <Field component={renderField} type={"text"} name="start_date"
                                           className="input-control"/>
                                </div>
                            </fieldset>
                            <fieldset>
                                <label>Date to</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <Field component={renderField} type={"text"} name="end_date"
                                           className="input-control"/>

                                </div>
                                <span className="till-today">
									<input type="radio" name="is_pursuing" checked/>
									Till Today
								</span>
                            </fieldset>
                        </div>

                        <div className="flex-container">
                            <fieldset>
                                <label>Description</label>
                                <textarea rows="3" placeholder="" name=""></textarea>
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


export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
