import React, {Component} from 'react';
import './language.scss'
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import PreviewModal from "../../../Preview/previewModal";
import renderLanguage from "./renderLanguage";
import validate from "../../../../../FormHandler/validtaions/language/validate"
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);
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
        this.props.fetchUserLanguage();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[8].entity_text})
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            console.log("I ma here")
            this.props.headingChange(this.props.personalInfo,8,e.target.value)
            this.setState({editHeading:false,heading:e.target.value})
        }
        if(key === 'blur'){
            console.log("I ma here")
            this.props.headingChange(this.props.personalInfo,8,e.target.value)
            this.setState({editHeading:false,heading:e.target.value})
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
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            //console.log("Came Here")
        }
        else{
            await this.props.bulkUpdateUserLanguage(values.list);
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
        
    }

    handleAddition(fields, error) {

        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: fields.length
        })
        scroller.scrollTo(`language${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 0
        })
    }

    deleteLanguage(index, fields, event) {
        event.stopPropagation();
        const language = fields.get(index);
        fields.remove(index);
        if (language && language.id) {
            this.props.removeLanguage(language.id)
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
        await this.props.bulkUpdateUserLanguage(fields.getAll());
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
        await this.props.bulkUpdateUserLanguage(fields.getAll());
    }


    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit, language,submitting,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.handleAddition}
                                deleteLanguage={this.deleteLanguage}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderLanguage}
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

export const LanguageForm = reduxForm({
    form: 'Language',
    enableReinitialize: true,
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
            return dispatch(actions.bulkUpdateUserLanguage({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
