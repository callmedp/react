import React, {Component} from 'react';
import './language.scss'
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderLanguage from "./renderLanguage";
import validate from "../../../../../FormHandler/validtaions/language/validate"
import {siteDomain} from "../../../../../../Utils/domains";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' :false
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[8].entity_text})
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,8,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,8,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[8].entity_text})
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
        await this.props.bulkUpdateUserLanguage(values);
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
            const form_data = this.props.info.form.language;
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
                await this.props.bulkUpdateUserLanguage(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss();
    }

    deleteLanguage(index, fields, event) {
        event.stopPropagation();
        const language = fields.get(index);
        fields.remove(index);
        if (language && language.id) {
            this.props.removeLanguage(language.id)
        }
    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit,submitting,personalInfo:{subscription_status},history,changeOrderingUp,changeOrderingDown} = this.props;
        const {editHeading,heading} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteLanguage={this.deleteLanguage}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                component={renderLanguage}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                context={this}
                                heading ={heading}/>
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

export const LanguageForm = reduxForm({
    form: 'language',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'language',-100),
    validate
})(Language);


const mapStateToProps = (state) => {
    return {
        initialValues: state.language,
        language: state.language
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserLanguage": () => {
            return dispatch(actions.fetchUserLanguage())
        },
        "removeLanguage": (languageId) => {
            return dispatch(actions.deleteLanguage(languageId))
        },

        "bulkUpdateUserLanguage": (listItems) => {
            listItems = (listItems || []).map(item => {
                const {proficiency} = item;
                if (!item['id']) delete item['id'];
                return item;
            })
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserLanguage({list: listItems,resolve,reject}))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
