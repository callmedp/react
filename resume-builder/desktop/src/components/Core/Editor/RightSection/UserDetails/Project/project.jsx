import React, {Component} from 'react';
import './project.scss'
import {Field, FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/projectValidation"
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';


class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,

        }
    }

    componentDidMount() {
        this.props.fetchUserProject()

    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=reference')
    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        console.log('donw pressed');
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem])
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('up pressed');
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        if (listLength) this.handleAccordionState(listLength, fields);
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


    handleAccordionState(val, fields) {
        const {currentAccordion} = this.state;

        if (currentAccordion !== '') {

            this.props.onSubmit(fields.get(currentAccordion))
        }

        this.setState((state) => ({
            previousAccordion: state.currentAccordion,
            openedAccordion: val,
            currentAccordion: val
        }))
    }

    handleAccordionClick(value, fields) {
        const val = value.length > 0 ? value[0] : ''
        this.handleAccordionState(val, fields)
    }


    render() {
        const {handleSubmit, project} = this.props;
        const renderProjects = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                <div>
                    <section className="head-section">
                        <span className="icon-box"><i className="icon-projects1"></i></span>
                        <h2>Projects</h2>
                        <span className="icon-edit icon-projects__cursor"></span>
                        <button
                            onClick={() => this.handleAddition(fields, error)}
                            type={'button'}
                            className="add-button add-button__right">Add new
                        </button>
                        {(touched || submitFailed) && error && <span>{error}</span>}
                    </section>
                    <section className="right-sidebar-scroll">
                        <ul>
                            <Accordion onChange={(value) => this.handleAccordionClick(value, fields, error)}
                                       allowZeroExpanded={true}
                                       preExpanded={[this.state.openedAccordion]}>
                                {
                                    fields.map((member, index) => {
                                        return (
                                            <li key={index}>
                                                <section className="info-section">
                                                    <AccordionItem uuid={index}>
                                                        <AccordionItemHeading>
                                                            <AccordionItemButton>
                                                                <div className="flex-container">
                                                                    <h3 className="add-section-heading">{fields.get(index).project_name || 'Project'}</h3>
                                                                    <div className="addon-buttons mr-10">
                                                                    <span
                                                                        onClick={(event) => this.deleteProject(index, fields, event)}
                                                                        className="icon-delete mr-15"/>
                                                                        {index !== 0 &&
                                                                        <span
                                                                            onClick={(event) => this.changeOrderingUp(index, fields, event)}
                                                                            className="icon-ascend mr-5"/>
                                                                        }
                                                                        {
                                                                            index !== fields.length - 1 &&
                                                                            < span
                                                                                onClick={(event) => this.changeOrderingDown(index, fields, event)}
                                                                                className="icon-descend"/>
                                                                        }
                                                                    </div>
                                                                </div>
                                                            </AccordionItemButton>
                                                        </AccordionItemHeading>
                                                        <AccordionItemPanel>
                                                            <div className="flex-container">
                                                                <fieldset>
                                                                    <label>Project Name</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-projects-gr"></span>
                                                                        </div>
                                                                        <Field component={renderField} type={"text"}
                                                                               name={`${member}.project_name`}
                                                                               className={"input-control"}/>
                                                                    </div>
                                                                </fieldset>
                                                            </div>
                                                            <div className="flex-container">
                                                                <fieldset>
                                                                    <label>Date from</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-date"></span>
                                                                        </div>
                                                                        <Field component={datepicker} type={"date"}
                                                                               className={'input-control'}
                                                                               name={`${member}.start_date`}/>
                                                                    </div>
                                                                </fieldset>
                                                                <fieldset>
                                                                    <label>Date to</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-date"></span>
                                                                        </div>
                                                                        <Field component={datepicker} type={"date"}
                                                                               className={'input-control'}
                                                                               name={`${member}.end_date`}/></div>
                                                                    <span className="till-today">
                                    <Field type="radio" name={`${member}.currently_working`} component="input"
                                           value={`${member}.currently_working`}/>
                                    Till Today
                                    </span>
                                                                </fieldset>
                                                            </div>

                                                            <div className="flex-container">
                                                                <fieldset>
                                                                    <label>Description</label>
                                                                    <Field component={renderTextArea} rows={"3"}
                                                                           type={"text"}
                                                                           name={`${member}.description`}
                                                                           value={`${member}.description`}/>
                                                                </fieldset>
                                                            </div>

                                                        </AccordionItemPanel>
                                                    </AccordionItem>
                                                </section>

                                            </li>
                                        )
                                    })
                                }

                            </Accordion>
                        </ul>
                    </section>
                </div>
            )
        }
        return (
            <div>

                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderProjects}/>
                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>
            </div>
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

        "handleSwap": (listItems) => {
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
            return dispatch(actions.handleProjectSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
