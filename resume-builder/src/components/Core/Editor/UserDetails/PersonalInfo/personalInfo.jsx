import React, {Component} from 'react';
import './personalInfo.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField} from "../../../../FormHandler/formFieldRenderer";

export class PersonalInfo extends Component {

    componentDidMount() {
        this.props.fetchPersonalInfo()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting} = this.props;
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-info1"></i></span>
                    <h2>Personal Info</h2>
                    <span className="icon-edit icon-edit__cursor"></span>
                </section>
                <form onSubmit={handleSubmit}>

                    <section className="flex-container right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>First Name</label>
                                    <Field component={renderField} type={"text"} name="first_name"/>
                                    <span class="error-txt"></span>
                                </fieldset>
                                <fieldset>
                                    <label>Last Name</label>
                                    <Field component={renderField} type={"text"} name="last_name"/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Designation</label>
                                    <Field component={renderField} type={"text"} name="designation"/>
                                </fieldset>
                                <fieldset>
                                    <label>Company</label>
                                    <Field component={renderField} type={"text"} name="company"/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Mobile</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-mobile"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="mobile"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Email</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-email"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="email"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Address</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-address"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="address"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Linkedin</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-linkedin"></span>
                                        </div>
                                        <input type="text" placeholder="" className="input-control"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Facebook</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-facebook"></span>
                                        </div>
                                        <input type="text" placeholder="" className="input-control"/>
                                    </div>
                                </fieldset>
                            </div>


                        </section>

                        <section className="pic-section mt-30">
                            <img className="img-responsive" src="/images/upload-image.jpg"/>
                        </section>
                    </section>
                </form>


                <div class="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button">Save & Continue</button>
                </div>

            </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo'
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        // "onSubmit": (personalDetails) => {
        //     return new Promise((resolve, reject) => {
        //         dispatch(actions.savePersonalInfo({personalDetails, resolve, reject}));
        //     })
        // }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
