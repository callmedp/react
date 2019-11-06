import React, {Component} from 'react';
import './language.scss'
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderLanguage from "./renderLanguage";
import validate from "../../../../../FormHandler/validtaions/language/validate"
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';

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
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[8].entity_text})
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
        let {sidenav:{listOfLinks,currentLinkPos},bulkUpdateUserLanguage,generateResumeAlert,updateCurrentLinkPos,
                history} = this.props
        currentLinkPos++
        
        this.setState({submit:true})
        await bulkUpdateUserLanguage(values);
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            generateResumeAlert()
        }
        else{
            updateCurrentLinkPos({currentLinkPos})
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    async updateInfoBeforeLoss(){

        if(!this.state.submit){
            const {initialValues} =this.props
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
            
            if(!error && JSON.stringify(initialValues)!==JSON.stringify(form_data['values'])){
                
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
        const {updateAlertModalStatus,handleSubmit,submitting,personalInfo:{order_data,entity_preference_data},headingChange,history,changeOrderingUp,changeOrderingDown,eventClicked} = this.props;
        const {editHeading,heading} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <Subscribe {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteLanguage={this.deleteLanguage}
                                changeOrderingUp={changeOrderingUp}
                                changeOrderingDown={changeOrderingDown}
                                eventClicked={eventClicked}
                                component={renderLanguage}
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
                                order_data={order_data} eventClicked={eventClicked} form_name={'Languages'}/>
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
