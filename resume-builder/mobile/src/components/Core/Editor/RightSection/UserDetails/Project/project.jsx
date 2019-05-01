import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/project/actions";
import {connect} from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/previewModal";
import validate from "../../../../../FormHandler/validtaions/project/validate"
import renderProjects from "./renderProject"
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

class Project extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : ''
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.editHeadingClick = this.editHeadingClick.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserProject()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[3].entity_text})
        }

    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,0,e.target.value)
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
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        await this.props.bulkUpdateUserProject(values.list);
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            this.props.history.push(`/resume-builder/buy`)
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
    }

    handleAddition(fields, error) {
        fields.push({
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "skills": [],
            "description": '',
            order: fields.length
        })
        scroller.scrollTo(`project${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 200
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

    async changeOrderingUp(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
        await this.props.bulkUpdateUserProject(fields.getAll());
    }

    async changeOrderingDown(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
        await this.props.bulkUpdateUserProject(fields.getAll());
    }

    render () {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit, project,submitting,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.handleAddition}
                                deleteProject={this.deleteProject}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderProjects}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                heading ={heading}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting || submitSucceeded} type={'submit'}>
                                    {(length === pos +1) ?"Buy" :"Save & Continue"}
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
