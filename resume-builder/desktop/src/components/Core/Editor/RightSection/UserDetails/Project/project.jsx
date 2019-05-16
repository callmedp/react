import React, {Component} from 'react';
import {FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/project/validate"
import {ProjectRenderer} from "./projectRenderer";

class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],
        };
        this.props.currentForm('project');

    }

    componentDidMount() {
        this.props.fetchUserProject()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.currently_working)
        }
        this.setState({till_today})

    }

    componentDidUpdate(prevProps) {
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.currently_working)
            }
            this.setState({till_today})
        }
    }


    componentWillUnmount() {
        let {formData: {project: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list'])

    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "skills": '',
            "currently_working": false,
            "description": '',
            order: listLength,
        })
    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state
        till_today[parseInt(index)] = checked
    }

    deleteProject(index, fields, event) {
        event.stopPropagation();
        const project = fields.get(index);
        fields.remove(index);
        if (project && project.id) {
            this.props.removeProject(project.id)
        }


    }

    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }


    render() {
        const {
            handleSubmit, ui: {loader}, saveTitle,
            editHeading, isEditable, entityName, nextEntity,
            handlePreview, changeOrderingDown, changeOrderingUp, formData: {project}
        } = this.props;
        const {till_today} = this.state
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name="list"
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAddition={this.handleAddition}
                    deleteProject={this.deleteProject}
                    changeOrderingUp={changeOrderingUp}
                    changeOrderingDown={changeOrderingDown}
                    loader={loader}
                    component={ProjectRenderer}
                    saveTitle={(event) => saveTitle(event, 3)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}
                    till_today={till_today}
                    tillTodayDisable={this.tillTodayDisable}
                    formValues={project && project.values}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type={'button'} onClick={handlePreview}>Preview</button>
                    <button className="orange-button"
                            type={'submit'}>{!nextEntity ? "Download" : 'Save and Continue'}</button>
                </div>
            </form>

        )
    }
}


export const ProjectForm = reduxForm({
    form: 'project',
    enableReinitialize: true,
    validate
})(Project);


const mapStateToProps = (state) => {
    return {
        initialValues: state.project,
        ui: state.ui,
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


        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userProject, index) => {
                const {start_date, end_date} = userProject;
                if (!userProject['id']) delete userProject['id'];
                userProject = {
                    ...userProject,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                        order: index
                    }
                };
                return userProject;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserProject({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
