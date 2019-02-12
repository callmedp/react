import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {
    renderField,
    required,
    datePicker,
    renderSelect,
    renderTextArea,
    phoneNumber
} from '../../../fieldLevelValidationForm';

export class Detail extends React.Component {
    constructor(props) {
        super(props);
    }

    genderOptions() {
        return [
            {value: 'M', label: 'Male'},
            {value: 'F', label: 'Female'},
            {value: 'O', label: 'Other'}
        ]
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting} = this.props;
        return (
            <div className="container pr">
                <header className="login-page-bg">
                    <div className="login-bg-txt">
                        <figure className="login-icon1"></figure>
                        <strong>1 Lacs+</strong>
                        Satisfied users
                    </div>
                    <div className="login-bg-txt">
                        <figure className="login-icon2"></figure>
                        <strong>300+</strong>
                        Courses
                    </div>
                    <div className="login-bg-txt">
                        <figure className="login-icon3"></figure>
                        <strong>500+</strong>
                        Professional resumes delivered
                    </div>
                </header>

                <div className="register login-signup-box">
                    <h1 className="modal-title">Add Your Information</h1>

                    <form onSubmit={handleSubmit}>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field name="date_of_birth" component={datePicker} validate={required}
                                       label="Date Of Birth"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="text" name="location" component={renderField} validate={required}
                                       label="Location"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field
                                    name="gender"
                                    component={renderSelect}
                                    validate={required}
                                    label="Gender"
                                    options={[
                                        {value: 'M', label: 'Male'},
                                        {value: 'F', label: 'Female'},
                                        {value: 'O', label: 'Other'}
                                    ]}
                                />

                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field
                                    name="extra_info"
                                    component={renderTextArea}
                                    type="text"
                                    label="Extra Information:"
                                />
                            </div>
                        </div>
                        <div className={'Button-group'}>
                            <div className={'Button-parent'}>
                                <button className={'Submit-button'} onClick={() => {
                                    this.props.history.goBack()
                                }}>
                                    Back
                                </button>
                            </div>
                            <div className={'Button-parent'}>
                                <button className={'Submit-button'} type="submit" disabled={pristine || submitting}>
                                    Next
                                </button>
                            </div>
                        </div>
                    </form>
                    {error && <div className={'Api-error'}>
                        <span>{error}</span>
                    </div>
                    }
                </div>
            </div>
        );
    }
}


export const DetailForm = reduxForm({
    form: 'detailForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/experience'
        })
    }
})(Detail);


const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userDetails) => {
            return new Promise((resolve, reject) => {

                dispatch(actions.updateUserDetails({userDetails, resolve, reject}))
            })
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(DetailForm);

