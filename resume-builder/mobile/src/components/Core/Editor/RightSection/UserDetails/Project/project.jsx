import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import { connect } from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/changeTemplateModal";
import validate from "../../../../../FormHandler/validtaions/project/validate"
import renderProjects from "./renderProject"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';

class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteProject = this.deleteProject.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false,
            'till_today': [],
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserProject()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.currently_working)
        }
        this.setState({ till_today })
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[3].entity_text })
        }

    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let { till_today } = this.state
        till_today[parseInt(index)] = checked
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[3].entity_text })
        }
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.currently_working)
            }
            this.setState({ till_today })
        }
    }

    editHeadingClick() {
        this.setState({ editHeading: true })
        this.props.sendTrackingInfo('right_section_edit',1)
    }

    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserProject, generateResumeAlert, updateCurrentLinkPos,
            history } = this.props
        currentLinkPos++
        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;

            values.map(el => {
                if (!el.project_name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserProject(values);
            }
        }
        this.setState({ submit: true })

        if (currentLinkPos === listOfLinks.length) {
            currentLinkPos = 0
            generateResumeAlert()
        }
        else {
            updateCurrentLinkPos({ currentLinkPos })
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
    }

    async updateInfoBeforeLoss() {

        if (!this.state.submit) {
            const { initialValues } = this.props
            const form_data = this.props.info.form.project;
            let error = false
            let error_values = form_data["syncErrors"]
            if (error_values) {
                for (let i of error_values['list']) {
                    for (let j of Object.keys(i)) {
                        if (i[j]) {
                            error = true
                            break;
                        }
                    }
                }
            }
            if (!error && JSON.stringify(initialValues) !== JSON.stringify(form_data['values'])) {

                const values = this.props.handleOrdering(form_data['values'])
                await this.props.bulkUpdateUserProject(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    deleteProject(index, fields, event) {
        event.stopPropagation();
        const project = fields.get(index);
        fields.remove(index);
        if (project && project.id) {
            this.props.removeProject(project.id)
        }


    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { updateAlertModalStatus, handleSubmit, submitting, personalInfo: { order_data, entity_preference_data },
            headingChange, history, changeOrderingUp, changeOrderingDown, eventClicked, showAlertMessage
        } = this.props;
        const { editHeading, heading, till_today } = this.state;
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props} />
                    <Subscribe {...this.props} />
                    <FieldArray name="list"
                        handleSubmit={handleSubmit}
                        handleAddition={this.props.handleAddition}
                        deleteProject={this.deleteProject}
                        changeOrderingUp={changeOrderingUp}
                        changeOrderingDown={changeOrderingDown}
                        eventClicked={eventClicked}
                        component={renderProjects}
                        headingChange={headingChange}
                        entity_preference_data={entity_preference_data}
                        editHeading={editHeading}
                        editHeadingClick={this.editHeadingClick}
                        context={this}
                        heading={heading}
                        till_today={till_today}
                        tillTodayDisable={this.tillTodayDisable}
                        showAlertMessage={showAlertMessage}
                    />
                    <ul className="form">
                        <li className="form__group">
                            <BottomCTC disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
                                length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                                order_data={order_data} eventClicked={eventClicked} form_name={'Projects'} />
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const ProjectForm = reduxForm({
    form: 'project',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'project', -100),
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
            const { start_date, end_date } = userProject;

            userProject = {
                ...userProject,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserProject({ userProject, resolve, reject }));
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
                const { start_date, end_date } = userProject;
                if (!userProject['id']) delete userProject['id'];
                userProject = {
                    ...userProject,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null
                    }
                };
                return userProject;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserProject({ list: listItems, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
