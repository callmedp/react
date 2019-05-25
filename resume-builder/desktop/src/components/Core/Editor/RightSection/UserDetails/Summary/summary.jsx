import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {hideSuggestionModal, showSuggestionModal} from '../../../../../../store/ui/actions/index';
import SuggestionModal from '../../../../../Modal/suggestionModal'

import {Field, reduxForm} from 'redux-form';
import styles from './summary.scss'


import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import LoaderSection from "../../../../../Loader/loaderSection.jsx";


class Summary extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            submit: false
        };
        this.props.currentForm('summary');

    }

    componentDidMount() {
        this.props.fetchPersonalInfo()

    }

    async handleSubmit(values, entityLink) {
        await this.props.onSubmit(values);
        this.setState({
            submit: true
        })
        if (entityLink) this.props.history.push(entityLink);
        else this.props.history.push('/resume-builder/buy/')
    }


    componentWillUnmount() {
        let {formData: {summary: {values}}} = this.props;
        if (!this.state.submit) this.props.onSubmit(values)
    }


    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return true;
    }


    render() {
        const {personalInfo: {extra_info}, ui: {loader, suggestionModal}, handleSubmit, handlePreview, isEditable, editHeading, saveTitle, entityName, nextEntity, showSuggestionModal} = this.props;
        let elem = null;
        return (
            <div>
                <SuggestionModal {...this.props} />
                <section className="head-section">
                    <span className="icon-box"><i className="icon-summary1"/></span>
                    <h2 className={"comp-heading"}
                        ref={(value) => {
                            elem = value
                        }} onKeyUp={(event) => saveTitle(event, 5)}
                        contenteditable={!!(isEditable) ? "true" : "false"}>{entityName}</h2>
                    <span onClick={() => editHeading(elem)}
                          className={!!(!isEditable) ? "icon-edit " + styles['icon-summary__cursor'] : ''}/>
                </section>
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                    <section className="right-sidebar-scroll p3p">
                        <div className={styles['summary-box']}>
                            <h3>Summary</h3>
                            <Field
                                noIcon={true}
                                component={renderTextArea} type={"textarea"} name="extra_info"
                                className="summary-box--summary-txt" rows="10" value={extra_info}/>
                        </div>
                        <span className="add-suggested" onClick={showSuggestionModal}>Add suggested summary</span>

                    </section>


                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-20" type={'button'} onClick={handlePreview}>Preview</button>
                        <button className="orange-button"
                                type={'submit'}>{!nextEntity ? "Download" : 'Save and Continue'}</button>
                    </div>
                </form>
            </div>
        )
    }
}


export const SummaryForm = reduxForm({
    form: 'summary',
    enableReinitialize: true
})(Summary);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails;
            personalDetails = {
                ...personalDetails,
                ...{
                    'gender': gender && gender['value'] || '',
                    'extracurricular': (extracurricular || []).map(el => el.value).join(',')
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "hideSuggestionModal": () => {
            return dispatch(hideSuggestionModal())
        },
        "showSuggestionModal": () => {
            return dispatch(showSuggestionModal())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SummaryForm);
