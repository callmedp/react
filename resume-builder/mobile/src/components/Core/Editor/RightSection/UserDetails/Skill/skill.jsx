import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validtaions/skill/validate"
import PreviewModal from "../../../Preview/previewModal";
import renderSkills from "./renderSkill"
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

class Skill extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteSkill = this.deleteSkill.bind(this)
        this.handleAddition = this.handleAddition.bind(this)
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
        this.props.fetchUserSkill();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[4].entity_text})
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            console.log("I ma here")
            this.props.headingChange(this.props.personalInfo,4,e.target.value)
            this.setState({editHeading:false,heading:e.target.value})
        }
        if(key === 'blur'){
            console.log("I ma here")
            this.props.headingChange(this.props.personalInfo,4,e.target.value)
            this.setState({editHeading:false,heading:e.target.value})
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[4].entity_text})
        }
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }

    deleteSkill(index, fields, event) {
        event.stopPropagation();
        ////console.log(index)
        ////console.log(fields.get(index))
        const skill = fields.get(index);
        fields.remove(index);
        if (skill && skill.id) {
            this.props.removeSkill(skill.id)
        }
    }

    handleAddition(fields) {
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": '',
            "order": fields.length
        })
        
        scroller.scrollTo(`skill${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
        })

    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            //console.log("Came Here")
        }
        else{
            await this.props.bulkSaveUserSkill(values.list);
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
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
        await this.props.bulkSaveUserSkill(fields.getAll());
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
        await this.props.bulkSaveUserSkill(fields.getAll());
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, skill,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    {error}
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.handleAddition}
                                deleteSkill={this.deleteSkill}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderSkills}
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
                                <button className="btn btn__round btn__primary" disabled={submitting || submitSucceeded} type={(length === pos +1) ?'button' :'submit'}
                                    onClick={(length === pos +1) ? ()=>{this.props.history.push(`/resume-builder/buy`)} : ()=>{}}>
                                    {(length === pos +1) ?"Buy" :"Save &amp; Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
            
        )
    }
}

export const SkillForm = reduxForm({
    form: 'Skill',
    validate,
    enableReinitialize: true
})(Skill);


const mapStateToProps = (state) => {
    return {
        initialValues: state.skill,
        skill: state.skill
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserSkill": () => {
            return dispatch(actions.fetchUserSkill())
        },
        "removeSkill": (skillId) => {
            return dispatch(actions.deleteSkill(skillId))
        },
        "bulkSaveUserSkill": (listItems) => {
            listItems = (listItems || []).map(userSkill => {
                const {proficiency} = userSkill;
                if (!userSkill['id']) delete userSkill['id'];
                return userSkill;
            })
            return dispatch(actions.bulkSaveUserSkill({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
