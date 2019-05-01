import React, {Component} from 'react';
import './project.scss'
import {Field, FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/project/validate"
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';
import Loader from "../../../../../Loader/loader.jsx";

const ProjectRenderer = ({
                             fields,
                             loader,
                             meta: {touched, error, submitFailed},
                             deleteProject,
                             handleSubmit,
                             handleAddition,
                             handleAccordionState,
                             handleAccordionClick,
                             changeOrderingUp,
                             changeOrderingDown,
                             openedAccordion,
                             editHeading,
                             saveTitle,
                             isEditable,
                             entityName
                         }) => {
    let elem = null;

    return (
        <div>
            {!!loader &&
            <Loader/>
            }
            <section className="head-section">
                <span className="icon-box"><i className="icon-projects1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}>{entityName}
                </h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-edit__cursor" : ""}></span>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className="add-button add-button__right">Add new
                </button>

            </section>
            <section className="right-sidebar-scroll">
                <ul>
                    <Accordion onChange={(value) => handleAccordionClick(value, fields, error)}
                               allowZeroExpanded={true}
                               preExpanded={[openedAccordion]}>
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).project_name || 'Project'}
                                                                <strong>1</strong></h3>
                                                            <div className="addon-buttons mr-10">
                                                                    <span
                                                                        onClick={(event) => deleteProject(index, fields, event)}
                                                                        className="icon-delete mr-15"/>
                                                                {index !== 0 &&
                                                                <span
                                                                    onClick={(event) => changeOrderingUp(index, fields, event)}
                                                                    className="icon-ascend mr-5"/>
                                                                }
                                                                {
                                                                    index !== fields.length - 1 &&
                                                                    < span
                                                                        onClick={(event) => changeOrderingDown(index, fields, event)}
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
                                                                    <span className="icon-projects-gr"/>
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
                                                                    <span className="icon-date"/>
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
                                                                    <span className="icon-date"/>
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
            isEditable: false
        }
    }

    componentDidMount() {
        this.props.fetchUserProject()

    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }

    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem])
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
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
        const {handleSubmit, ui: {loader}, saveTitle, editHeading, isEditable, entityName, nextEntity} = this.props;
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name="list"
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAccordionState={this.handleAccordionState}
                    handleAddition={this.handleAddition}
                    deleteProject={this.deleteProject}
                    changeOrderingUp={this.changeOrderingUp}
                    changeOrderingDown={this.changeOrderingDown}
                    openedAccordion={this.state.openedAccordion}
                    loader={loader}
                    component={ProjectRenderer}
                    saveTitle={(event) => saveTitle(event, 3)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button" type={'submit'}>Save & Continue</button>
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
