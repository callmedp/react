import React, {Component} from 'react';
import {FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/project/validate"
import {ProjectRenderer} from "./projectRenderer";
import {scroller} from "react-scroll/modules";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import {siteDomain} from '../../../../../../Utils/domains'

class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],
        };
        this.props.currentForm('project');

    }

    componentDidMount() {

        // document.getElementsByClassName('react-datepicker__current-month')[0].style.display = "none"

        this.props.fetchUserProject()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.currently_working)
        }
        this.setState({till_today})

    }

    async componentDidUpdate(prevProps){
        const {ui:{previewClicked},previewButtonClicked,history,initialValues} = this.props;
        if(previewClicked !== prevProps.ui.previewClicked && previewClicked){
            await this.updateInfoBeforeLoss()
            this.setState({submit:true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
        if (initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of initialValues.list) {
                till_today.push(i.currently_working)
            }
            this.setState({till_today})
        }
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    async handleSubmit(values, entityLink) {
         const {userInfo:{order_data},hideGenerateResumeModal,showGenerateResumeModal,history,reGeneratePDF} = this.props
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else if(order_data && order_data.id){
            showGenerateResumeModal()
            reGeneratePDF(order_data.id)
            setTimeout(function() {
                window.location.href = `${siteDomain}/dashboard`
                hideGenerateResumeModal()
            }, 10000);
        }
        else{
            history.push(`/resume-builder/buy`) 
        }
        }

    }

    

    async updateInfoBeforeLoss(){
        let { initialValues, formData: {project: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}     ).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues)!==JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "currently_working": false,
            "description": '',
            order: listLength,
        })

        scroller.scrollTo(`project${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 400,
            containerId: 'project'
        })
        this.props.eventClicked({
            'action':'AddNew',
            'label':'Projects'
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
            handleSubmit,userInfo:{order_data}, ui: {loader}, saveTitle,
            editHeading, isEditable, entityName, nextEntity,eventClicked,
            showAlertModal,history, changeOrderingDown, changeOrderingUp, handleInputValue, formData: {project}
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
                    saveTitle={(event) => saveTitle(event, 4)}
                    editHeading={() => editHeading(4)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}
                    till_today={till_today}
                    tillTodayDisable={this.tillTodayDisable}
                    formValues={project && project.values}
                    handleInputValue={handleInputValue}

                />

                <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'Projects'}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
                    />
            </form>

        )
    }
}


export const ProjectForm = reduxForm({
    form: 'project',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'project',-100),
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
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
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
