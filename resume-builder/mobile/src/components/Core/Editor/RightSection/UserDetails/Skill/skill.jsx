import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validtaions/skill/validate"
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderSkills from "./renderSkill"
import {siteDomain} from "../../../../../../Utils/domains";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';

class Skill extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteSkill = this.deleteSkill.bind(this)

        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : ''
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserSkill();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[4].entity_text})
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
        const skill = fields.get(index);
        fields.remove(index);
        if (skill && skill.id) {
            this.props.removeSkill(skill.id)
        }
    }

    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let {sidenav:{listOfLinks,currentLinkPos},bulkSaveUserSkill,personalInfo:{order_data},updateCurrentLinkPos,history,showGenerateResumeModal,hideGenerateResumeModal,reGeneratePDF} = this.props
        currentLinkPos++
        this.setState({submit:true})
        await bulkSaveUserSkill(values);
         if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            if(order_data && order_data.id){
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
        else{
            updateCurrentLinkPos({currentLinkPos})
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    async updateInfoBeforeLoss(){

        if(!this.state.submit){
            const {initialValues} =this.props
            const form_data = this.props.info.form.skill;
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
            if(!error && JSON.stringify(initialValues)!==JSON.stringify(form_data['values'])){
                
                const values = this.props.handleOrdering(form_data['values'])
                await this.props.bulkSaveUserSkill(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {updateAlertModalStatus, handleSubmit,submitting,personalInfo:{order_data,entity_preference_data},headingChange,history,changeOrderingDown,changeOrderingUp,eventClicked} = this.props;
        const {editHeading,heading} =this.state;
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteSkill={this.deleteSkill}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                eventClicked={eventClicked}
                                component={renderSkills}
                                headingChange={headingChange}
                                entity_preference_data={entity_preference_data}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                
                                context={this}
                                heading ={heading}/>
                    <ul className="form">
                        <li className="form__group">
                            <BottomCTC  disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
                                length={length} pos={pos+1} updateInfoBeforeLoss={this.updateInfoBeforeLoss} 
                                order_data={order_data} eventClicked={eventClicked} form_name={'Skills'}/>
                        </li>
                    </ul>
                </form>
            </div>
            
        )
    }
}

export const SkillForm = reduxForm({
    form: 'skill',
    validate,
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'skill',-100),
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
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkSaveUserSkill({list: listItems,resolve,reject}))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
