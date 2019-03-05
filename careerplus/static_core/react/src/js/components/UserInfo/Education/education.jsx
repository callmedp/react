import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Education extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        if (!userId) history.push('/resume-builder/register');
    }

    handleAddEducation(invalid, educations, educationValues, reset, userId) {
        if (invalid) return;
        let educationList = educations || [];

        educationList.push({
            ...educationValues,
            "course_type": educationValues['course_type'].value,


            user: userId
        })
        ;
        this.props.addEducation({educations: educationList});
        reset();

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, educations, educationValues, invalid, userId} = this.props;
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Add Your Qualifications</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="specialization" component={renderField} validate={required}
                                   label="Specialization"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="institution_name" component={renderField} validate={required}
                                   label="Institution Name"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="course_type"
                                   component={renderSelect}
                                   validate={required}
                                   options={[
                                       {value: 'FT', label: 'FULL TIME'},
                                       {value: 'PT', label: 'PART TIME'},
                                   ]}
                                   label="Course Type"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="percentage_cgpa" component={renderField} validate={required}
                                   label="Percentage/Cgpa"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="start_date" component={datePicker} validate={required}
                                   label="Start Date"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="end_date" component={datePicker} validate={required}
                                   label="End Date"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <div>
                                <label>Currently Pursuing</label>
                            </div>
                            <Field type="checkbox" name="is_pursuing" component={renderField} validate={required}
                                   label="Currently Pursuing"/>
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
                                this.handleAddEducation.bind(this, invalid, educations, educationValues, reset, userId)
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
                    !!(educations && educations.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>Educations:</span>
                        {
                            (educations || []).map(education => (
                                <button>{education['institution_name']}</button>
                            ))
                        }
                    </div>
                }
            </div>
        );
    }
}


export const EducationForm = reduxForm({
    form: 'educationForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/project'
        })
    }
})(Education);


const mapStateToProps = (state) => {
    return {
        educationValues: state.form && state.form.educationForm && state.form.educationForm.values || {},
        educations: state.userInfoReducer.educations,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userEducation) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserEducation({userEducation, resolve, reject}))
        }),
        "addEducation": (experience) => {
            return dispatch(actions.addEducation(experience))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);

