import React, {Component} from 'react';
import './personalInfo.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, datepicker} from "../../../../FormHandler/formFieldRenderer.jsx";
import DatePickerField from "../../../../FormHandler/formFieldRenderer.jsx";

export class PersonalInfo extends Component {

    componentDidMount() {
        this.props.fetchPersonalInfo()
        this.adaptFileEventToValue = this.adaptFileEventToValue.bind(this)
    }

    adaptFileEventToValue(e) {
        console.log(e.target.files[0]);
        this.props.fetchImageUrl(e.target.files[0]);

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;
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
                                    <span className="error-txt"></span>
                                </fieldset>
                                <fieldset>
                                    <label>Last Name</label>
                                    <Field component={renderField} type={"text"} name="last_name"/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Gender</label>
                                    <Field component={renderField} type={"text"} name="gender"/>
                                </fieldset>
                                <fieldset>
                                    <label>Date Of Birth</label>
                                    <Field component={datepicker} name="date_of_birth" className={"input-control"}/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Mobile</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-mobile"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="number"
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
                                        <Field component={renderField} type={"text"} name="location"
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
                                        <Field component={renderField} type={"text"} name="linkedIn"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Facebook</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-facebook"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="facebook"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>

                        </section>

                        <section className="pic-section mt-30">
                            <img className="img-responsive" src="/media/static/react/assets/images/upload-image.jpg"/>
                            <input
                                onChange={this.adaptFileEventToValue}
                                onBlur={this.adaptFileEventToValue}
                                type="file"
                                name="image"
                            />
                        </section>
                    </section>


                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type="submit" disabled={pristine || submitting}>Save &
                            Continue
                        </button>
                    </div>
                </form>


            </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "fetchImageUrl": (imageFile) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.fetchImageUrl({imageFile, resolve, reject}));
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
