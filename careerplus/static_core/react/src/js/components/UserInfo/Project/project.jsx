
import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {
    renderField,
    required,
    datePicker,
    renderDynamicSelect
} from '../../../fieldLevelValidationForm';

export class Project extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        if (!userId) history.push('/resume-builder/register');
    }

    async fetchSkillList(inputValue, callback) {
        try {
            const skills = await this.props.fetchSkills(inputValue);
            const listData = (skills && skills.results || []).map(skill => ({value: skill.id, label: skill.name}))
            callback(listData);
        } catch (e) {
            console.log('--error-', e);
        }
    }

    componentDidMount() {
        this.props.fetchDefaultSkills()
    }

    handleEndDateChange(date) {
        console.log('---endDate--', date);
    }

    handleStartDateChange(date) {
        console.log('---startDate---', date);
    }

    handleAddProject(invalid, projects, projectValues, reset, userId) {

        if (invalid) return;
        let projectList = projects || [];
        const {skills} = projectValues;
        const updatedSkills = (skills || []).map(skill => skill['value'])

        projectList.push({
            ...projectValues,
            skills: updatedSkills,
            user: userId
        })
        ;
        this.props.addProject({projects: projectList});
        reset();

    }


    render() {
        const {error, handleSubmit, pristine, reset, submitting, projects, projectValues, invalid, userId} = this.props;
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Add Your Projects</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="project_name" component={renderField} validate={required}
                                   label="Project Name"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="description" component={renderField} validate={required}
                                   label="Project Description"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="start_date" component={datePicker}
                                   validate={required}
                                   onDateChange={this.handleStartDateChange}
                                   label="Start Date"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="end_date" component={datePicker} validate={required}
                                   onDateChange={this.handleEndDateChange}
                                   label="End Date"/>
                        </div>
                    </div>

                    <div className={'Text-spacing'}>
                        <div>
                            <Field name="skills" component={renderDynamicSelect}
                                   loadOptions={this.fetchSkillList.bind(this)}
                                   defaultOptions={this.props.defaultSkills}
                                   label="Select Skills"/>
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
                                this.handleAddProject.bind(this, invalid, projects, projectValues, reset, userId)
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
                    !!(projects && projects.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>Projects:</span>
                        {
                            (projects || []).map(project => (
                                <button>{project['project_name']}</button>
                            ))
                        }
                    </div>
                }

            </div>
        );
    }
}


export const ProjectForm = reduxForm({
    form: 'projectForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/certification'
        })
    }
})(Project);


const mapStateToProps = (state) => {
    return {
        defaultSkills: state.skill.defaultList,
        projectValues: state.form && state.form.projectForm && state.form.projectForm.values || {},
        projects: state.userInfoReducer.projects,
        userId: state.userInfoReducer.id,
        initialValues: state.activeProject
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userProject) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.saveUserProject({userProject, resolve, reject}))
            })
        },
        "fetchSkills": (inputValue = '') => {
            return new Promise((resolve, reject) => {
                dispatch(actions.fetchSkillList({inputValue, resolve, reject}))
            });
        },
        "fetchDefaultSkills": (inputValue = '') => {
            return dispatch(actions.fetchDefaultSkillList(inputValue))
        },
        "addProject": (project) => {
            return dispatch(actions.addProject(project))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);

