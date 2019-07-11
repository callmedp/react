import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, phoneNumber} from '../../../fieldLevelValidationForm';

export class Register extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting} = this.props;
        const staticPath = '/media/static'
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Register</h1>
{/*
                <img src={`${staticPath}/react/assets/images/functional.jpg`}   />
*/}

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="first_name" component={renderField} validate={required}
                                   label="First Name:"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="last_name" component={renderField} validate={required}
                                   label="Last Name:"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="email"
                                component={renderField}
                                validate={required}
                                type="email"
                                label="Email:"
                            />
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="number"
                                component={renderField}
                                validate={[required, phoneNumber]}
                                type="text"
                                label="Contact Number:"
                            />
                        </div>
                    </div>
                    <div className={'Button-parent'}>
                        <button className={'Submit-button'} type="submit" disabled={pristine || submitting}>
                            Next
                        </button>
                    </div>
                </form>
                {error && <div className={'Api-error'}>
                    <span>{error}</span>
                </div>
                }
            </div>
        );
    }
}


export const RegisterForm = reduxForm({
    form: 'user_info',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/detail'
        })
    }
})(Register);


const mapStateToProps = (state) => {
    return {
        pinCode: state.userInfoReducer["pinCode"],

    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userDetails) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserDetails({userDetails, resolve, reject}))
        })
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(RegisterForm);

