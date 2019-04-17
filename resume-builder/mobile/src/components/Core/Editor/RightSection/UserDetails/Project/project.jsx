import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import {required} from "../../../../../FormHandler/formValidations"
class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserProject()

    }

    async handleSubmit(values) {
        await this.props.bulkUpdateUserProject(values.list);
        this.props.history.push('/resume-builder/edit/?type=reference')
    }

    handleAddition(fields, error) {
        fields.push({
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "skills": '',
            "description": '',
            order: listLength
        })
    }

    deleteProject(index, fields, event) {
        event.stopPropagation();
        const project = fields.get(index);
        fields.remove(index);
        if (project && project.id) {
            this.props.removeProject(project.id)
        }


    }

    render () {
        const {handleSubmit, project} = this.props;
        const renderProjects = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Project</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline"
                            onClick={() => this.handleAddition(fields, error)}
                            type={'button'}>+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                        return (
                            <React.Fragment>
                                <div className="subHeading pb-0">
                                    <h2>{project.project_name}</h2>
                                    <ul className="subHeading__control">
                                        <li className="subHeading__delete">
                                            <span className="sprite icon--delete" 
                                            onClick={(event) => this.deleteProject(index, fields, event)}
                                            role="button"></span>
                                        </li>
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--upArrow"></i>
                                        </li>
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--downArrow"></i>
                                        </li>
                                    </ul>
                                </div>

                                <ul className="form pb-0">
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="project_name">Project name </label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--project-gray"></i>
                                            </span>
                                            </div>
                                            <Field component={renderField} validate={required} type={"text"} 
                                            name={`${member}.project_name`} className="form__input"/>
                                        </div>
                                    </li>
                                    
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="start_date">Date from</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                            </div>
                                            <Field component={datepicker} validate={required} type={"date"} 
                                                className="form__input" name={`${member}.start_date`}/>
                                        </div>
                                    </li>
                                    
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="end_date">Date to</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                            </div>
                                            <Field component={datepicker} validate={required} type={"date"} 
                                                className="form__input" name={`${member}.end_date`}/>
                                        </div>
                                    </li>
                                    

                                    <li className="form__radio-group d-flex justify-content-end fs-14">
                                        <Field type="radio" name={`${member}.currently_working`} component="input"
                                            className="form__radio-input" value={`${member}.currently_working`}/>
                                        <label class="form__radio-label" htmlFor="currently_working">
                                            <span className="form__radio-button"></span>
                                            Till today
                                        </label>
                                    </li>

                                    <li className="form__group">
                                        <label className="form__label" htmlFor="description">Description</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                                <span className="input-group__text">
                                                    <i className="sprite icon--date"></i>
                                                </span>
                                            </div>
                                            <Field component={renderTextArea} rows={"3"} type={"textarea"}
                                                className="form__input" name={`${member}.description`}
                                                value={`${member}.description`}/>
                                        </div>
                                    </li>
                                </ul>
                            </React.Fragment>
                        )})}      
                </div>
            
            )
        }
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderProjects}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary" type={'submit'}>Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const ProjectForm = reduxForm({
    form: 'project',
    enableReinitialize: true
})(Project);


const mapStateToProps = (state) => {
    return {
        initialValues: state.project,
        project: state.project
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userProject) => {
            const {start_date, end_date} = userProject;

            userProject = {
                ...userProject,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserProject({userProject, resolve, reject}));
            })
        },
        "fetchUserProject": () => {
            return dispatch(actions.fetchUserProject())
        },
        "removeProject": (projectId) => {
            return dispatch(actions.deleteProject(projectId))
        },

        "bulkUpdateUserProject": (listItems) => {
            listItems = (listItems || []).map(userProject => {
                const {start_date, end_date} = userProject;
                if (!userProject['id']) delete userProject['id'];
                userProject = {
                    ...userProject,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                    }
                };
                return userProject;
            });
            return dispatch(actions.bulkUpdateUserProject({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
