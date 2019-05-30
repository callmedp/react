import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/changeTemplateModal";
import validate from "../../../../../FormHandler/validtaions/project/validate"
import renderProjects from "./renderProject"
import {siteDomain} from "../../../../../../Utils/domains";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"

class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteProject = this.deleteProject.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false,
            'till_today': [],
        }
        this.updateInputValue =this.updateInputValue.bind(this);
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
        this.setState({till_today})
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[3].entity_text})
        }

    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state
        till_today[parseInt(index)] = checked
    }


    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,3,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,3,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[3].entity_text})
        }
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.currently_working)
            }
            this.setState({till_today})
        }
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }

    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        this.setState({submit:true})
        await this.props.bulkUpdateUserProject(values);
         if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            if(this.props.personalInfo.subscription_status){
                window.location.href = `${siteDomain}/dashboard/myorder`
            }
            else{
                this.props.history.push(`/resume-builder/buy`) 
            }
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
    }

    async updateInfoBeforeLoss(){

        if(!this.state.submit){
            const form_data = this.props.info.form.project;
            let error = false
            let error_values =form_data["syncErrors"]
            if(error_values){
                for(let i of  error_values['list']){
                    for(let j of Object.keys(i)){
                        if(i[j]){
                            error =true
                            break;
                        }
                    }
                }
            }
            if(!error){
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

    render () {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit,submitting,personalInfo:{subscription_status},history,previewHandling,changeOrderingUp,changeOrderingDown} = this.props;
        const {editHeading,heading,till_today} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteProject={this.deleteProject}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                component={renderProjects}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                context={this}
                                heading ={heading}
                                till_today={till_today}
                                tillTodayDisable={this.tillTodayDisable}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                 <button className="btn btn__round btn--outline" 
                                    onClick={async()=>{previewHandling(this.updateInfoBeforeLoss,history);this.setState({submit:true}) }}
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                                </button>
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
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'project',-100),
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

        "bulkUpdateUserProject": (listItems) => {
            listItems = (listItems || []).map(userProject => {
                const {start_date, end_date} = userProject;
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
                return dispatch(actions.bulkUpdateUserProject({list: listItems,resolve,reject}))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
