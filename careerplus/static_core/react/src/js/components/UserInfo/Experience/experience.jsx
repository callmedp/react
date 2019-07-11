import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Experience extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        if (!userId) history.push('/resume-builder/register');
    }

    handleAddExperience(invalid, experiences, experienceValues, reset, userId) {
        if (invalid) return;
        let experienceList = experiences || [];
        experienceList.push({
            ...experienceValues,
            user: userId
        });
        this.props.addExperience({experiences: experienceList});
        reset();

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, experiences, experienceValues, invalid, userId} = this.props;
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Add Your Experience</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="job_profile" component={renderField} validate={required}
                                   label="Job Profile"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="company_name" component={renderField} validate={required}
                                   label="Company"/>
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
                                <label>Currently Working</label>
                            </div>
                            <Field type="checkbox" name="is_working" component={renderField} validate={required}
                                   label="Currently Working"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="job_location" component={renderField} validate={required}
                                   label="Job Location"/>
                        </div>
                    </div>

                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="work_description"
                                component={renderTextArea}
                                type="text"
                                label="Job Description"
                            />
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
                                this.handleAddExperience.bind(this, invalid, experiences, experienceValues, reset, userId)
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
                    !!(experiences && experiences.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>Experiences:</span>
                        {
                            (experiences || []).map(experience => (
                                <button>{experience['job_profile']}</button>
                            ))
                        }
                    </div>
                }
            </div>
        );
    }
}


export const ExperienceForm = reduxForm({
    form: 'experienceForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/education'
        })
    }
})(Experience);


const mapStateToProps = (state) => {
    return {
        experienceValues: state.form && state.form.experienceForm && state.form.experienceForm.values || {},
        experiences: state.userInfoReducer.experiences,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userExperiences) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserExperience({userExperiences, resolve, reject}))
        }),
        "addExperience": (experience) => {
            return dispatch(actions.addExperience(experience))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);

