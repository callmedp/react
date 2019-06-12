import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import validate from "../../../../../FormHandler/validtaions/education/validate";
import * as actions from "../../../../../../store/education/actions";
import {connect} from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderEducation from "./renderEducation"
import {siteDomain} from "../../../../../../Utils/domains";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';

class Education extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteEducation = this.deleteEducation.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false,
            'till_today': [],
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        this.setState({submit:true})
        await this.props.bulkUpdateUserEducation(values);
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

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state
        till_today[parseInt(index)] = checked
    }

    async updateInfoBeforeLoss(){

        if(!this.state.submit){
            
            const form_data = this.props.info.form.education;
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
                await this.props.bulkUpdateUserEducation(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }


    componentDidMount() {
        this.props.fetchUserEducation()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_pursuing)
        }
        this.setState({till_today})
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[1].entity_text})
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[1].entity_text})
        }
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.is_pursuing)
            }
            this.setState({till_today})
        }
    }

    deleteEducation(index, fields, event) {
        event.stopPropagation();
        const education = fields.get(index);
        fields.remove(index);
        if (education && education.id) {
            
            this.props.removeEducation(education.id)
        }
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit,submitting,personalInfo:{subscription_status,entity_preference_data},headingChange,history,changeOrderingUp,changeOrderingDown} = this.props;
        const {editHeading,heading,till_today} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}> 
                    <PreviewModal {...this.props}/>
                    <FieldArray name={'list'}
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteEducation={this.deleteEducation}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                component={renderEducation}
                                headingChange={headingChange}
                                entity_preference_data={entity_preference_data}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                heading ={heading}
                                context={this}
                                till_today={till_today}
                                tillTodayDisable={this.tillTodayDisable}/> 
                    <ul className="form">
                        <li className="form__group">
                         <BottomCTC  disabled={submitting} context={this} history={history}
                                length={length} pos={pos+1} updateInfoBeforeLoss={this.updateInfoBeforeLoss} 
                                subscription_status={subscription_status}/>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'education',-100),
    validate
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education,
        education: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
        "removeEducation": (educationId) => {
            return dispatch(actions.deleteEducation(educationId))
        },

        "bulkUpdateUserEducation": (listItems) => {
            listItems = (listItems || []).map(userEducation => {
                    const {start_date, end_date, course_type} = userEducation;
                    if (!userEducation['id']) delete userEducation['id'];
                    userEducation = {
                        ...userEducation,
                        ...{
                            start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                            end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || null,
                        }
                    };
                    return userEducation;
                }
            );
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserEducation({list: listItems,resolve,reject}))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
