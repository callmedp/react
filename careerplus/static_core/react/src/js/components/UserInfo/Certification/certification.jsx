import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Certification extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        if (!userId) history.push('/resume-builder/register');
    }


    handleAddCertification(invalid, certifications, certificationValues, reset, userId) {
        if (invalid) return;
        let certificationList = certifications || [];
        certificationList.push({
            ...certificationValues,
            user: userId
        });
        this.props.addCertification({certifications: certificationList});
        reset();

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, certifications, certificationValues, invalid, userId} = this.props;
        return (

            <div className="register login-signup-box">
                <h1 className="modal-title">Add Your Certifications</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="name_of_certification" component={renderField}
                                   validate={required}
                                   label="Name Of Certification"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="year_of_certification" component={datePicker}
                                   validate={required}
                                   label="Year Of Certification"/>
                        </div>
                    </div>

                    <div className={'Button-group'}>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button" onClick={() => {
                                this.props.history.goBack()
                            }}>
                                Back
                            </button>
                        </div>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button" onClick={
                                this.handleAddCertification.bind(this, invalid, certifications, certificationValues, reset, userId)
                            }>
                                Add
                            </button>
                        </div>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button">
                                Preview
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
                {
                    !!(certifications && certifications.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>Certifications:</span>
                        {
                            (certifications || []).map(certification => (
                                <button>{certification['name_of_certification']}</button>
                            ))
                        }
                    </div>
                }
            </div>
        );
    }
}


export const CertificationForm = reduxForm({
    form: 'certificationForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/achievement'
        })
    }
})(Certification);


const mapStateToProps = (state) => {
    return {
        certificationValues: state.form && state.form.certificationForm && state.form.certificationForm.values || {},
        certifications: state.userInfoReducer.certifications,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userCertification) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserCertification({userCertification, resolve, reject}))
        }),
        "addCertification": (certification) => {
            return dispatch(actions.addCertification(certification))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(CertificationForm);

