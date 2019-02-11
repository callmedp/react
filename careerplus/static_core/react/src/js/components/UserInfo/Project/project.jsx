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
    select
} from '../../../fieldLevelValidationForm';

export class Project extends React.Component {
    constructor(props) {
        super(props);
        this.fetchSkillList.bind(this);
        this.handleAddProject.bind(this);
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

    handleAddProject(formErrors, projects, projectValues, reset) {
        if (Object.keys(formErrors).length) return;
        let projectList = projects || [];
        projectList.push(projectValues);
        this.props.addProject({projects: projectList});
        reset();

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, projects, projectValues, formErrors} = this.props;
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
                                <Field type="date" name="start_date" component={renderField} validate={required}
                                       label="Start Date"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="date" name="end_date" component={renderField} validate={required}
                                       label="End Date"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field name="skills" component={select}
                                       loadOptions={this.fetchSkillList.bind(this)}
                                       defaultOptions={this.props.defaultSkills}
                                       label="End Date"/>
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
                                    this.handleAddProject.bind(this, formErrors, projects, projectValues, reset)
                                }>
                                    Add
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
                        projects && projects.length ?
                            (projects || []).map(project => (
                                <button>{project['project_name']}</button>
                            )) : ''
                    }
                </div>
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
        formErrors: state.form && state.form.projectForm && state.form.projectForm.syncErrors || {},
        projects: state.userInfoReducer.projects
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

