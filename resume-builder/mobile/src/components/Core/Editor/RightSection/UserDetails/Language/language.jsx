import React, { Component } from 'react';
import './language.scss'
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import { connect } from "react-redux";
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderLanguage from "./renderLanguage";
import validate from "../../../../../FormHandler/validtaions/language/validate"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';
import propTypes from 'prop-types';

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
    }
    
    componentDidMount() {
        this.props.fetchUserLanguage();
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[8].entity_text })
        }
    }
    
    
    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[8].entity_text })
        }
    }
    
    editHeadingClick() {
        this.setState({ editHeading: true })
    }
    
    
    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserLanguage, generateResumeAlert, updateCurrentLinkPos,
        history } = this.props
        currentLinkPos++
        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            
            values.map(el => {
                if (!el.name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserLanguage(values);
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
            const form_data = this.props.info.form.language;
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
        const { updateAlertModalStatus, handleSubmit, submitting, personalInfo: { order_data, entity_preference_data }, headingChange,
        history, changeOrderingUp, changeOrderingDown, eventClicked, showAlertMessage
    } = this.props;
    const { editHeading, heading } = this.state;
    return (
        <div className="buildResume">
        <form onSubmit={handleSubmit(this.handleSubmit)}>
        <PreviewModal {...this.props} />
        <Subscribe {...this.props} />
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
        heading={heading}
        showAlertMessage={showAlertMessage}
        />
        <ul className="form">
        <li className="form__group">
        <BottomCTC disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
        length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
        order_data={order_data} eventClicked={eventClicked} form_name={'Languages'} />
        </li>
        </ul>
        </form>
        </div>
        )
    }
}

Language.propTypes = {
    bulkUpdateUserLanguage: propTypes.func,
    changeOrderingDown: propTypes.func,
    changeOrderingUp: propTypes.func,
    eventClicked: propTypes.func,          
    fetchUserLanguage: propTypes.func,
    form: propTypes.string,
    generateResumeAlert: propTypes.func,          
    handleAddition: propTypes.func,
    handleOrdering: propTypes.func,
    handleSubmit: propTypes.func,
    headingChange: propTypes.func,          
    history: propTypes.shape({
        action: propTypes.string,
        block: propTypes.func,
        createHref: propTypes.func,
        go: propTypes.func,
        goBack: propTypes.func,
        goForward: propTypes.func,
        length: propTypes.number,
        listen: propTypes.func,
        location: propTypes.shape({
            hash: propTypes.string,
            pathname: propTypes.string,
            search: propTypes.string,
            state: undefined
        }),
        push: propTypes.func,
        replace: propTypes.func, 
    }),
    initialValues: propTypes.shape({
        currentLinkPos: propTypes.string,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    language: propTypes.shape({
        list: propTypes.array
    }),
    personalInfo: propTypes.shape({
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        gender: propTypes.string,
        hide_subscribe_button: propTypes.bool,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
    }),
    removeLanguage: propTypes.func,
    showAlertMessage: propTypes.func,
    sidenav: propTypes.shape({
        currentLinkPos: propTypes.string,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    submitting: propTypes.bool,
    updateAlertModalStatus: propTypes.func,
    updateCurrentLinkPos: propTypes.func,
}

export const LanguageForm = reduxForm({
    form: 'language',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'language', -100),
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
                const { proficiency } = item;
                if (!item['id']) delete item['id'];
                return item;
            })
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserLanguage({ list: listItems, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
