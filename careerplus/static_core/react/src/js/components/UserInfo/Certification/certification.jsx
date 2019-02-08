import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Certification extends React.Component {
    constructor(props) {
        super(props);
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
                    <h1 className="modal-title">Add Your Certifications</h1>

                    <form onSubmit={handleSubmit}>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="text" name="name_of_certification" component={renderField} validate={required}
                                       label="Name Of Certification"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="date" name="year_of_certification" component={renderField} validate={required}
                                       label="Year Of Certification"/>
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


export const CertificationForm = reduxForm({
    form: 'user_info',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/achievement'
        })
    }
})(Certification);


const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userCertification) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserCertification({userCertification, resolve, reject}))
        })
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(CertificationForm);

