import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {fetchUserExperience, fetchJobTitles} from '../../../../../../store/experience/actions/index';
import {hideSuggestionModal, showSuggestionModal} from '../../../../../../store/ui/actions/index';
import SuggestionModal from '../../../../../Modal/suggestionModal'

import {Field, reduxForm} from 'redux-form';
import styles from './summary.scss'


import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import {siteDomain} from '../../../../../../Utils/domains'


class Summary extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            submit: false,
            modal_status: false
        };
        this.props.currentForm('summary');

    }

    componentDidMount() {
        this.props.fetchPersonalInfo();
        this.props.fetchUserExperience();

    }

    async componentDidUpdate(prevProps) {
        const {ui: {previewClicked}, previewButtonClicked, history} = this.props;
        if (previewClicked !== prevProps.ui.previewClicked && previewClicked) {
            await this.updateInfoBeforeLoss()
            this.setState({submit: true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }

    async updateInfoBeforeLoss() {
        let {initialValues, formData: {summary: {values}}, personalInfo} = this.props;
        if (!this.state.submit && JSON.stringify(initialValues) !== JSON.stringify(values)) await this.props.onSubmit(values, personalInfo)
    }

    async handleSubmit(values, entityLink) {
        const {userInfo: {order_data}, hideGenerateResumeModal, showGenerateResumeModal, history, reGeneratePDF, personalInfo} = this.props;
        await this.props.onSubmit(values, personalInfo);
        this.setState({
            submit: true
        })
        if (entityLink) {
            this.props.history.push(entityLink)
        } else if (order_data && order_data.id) {
            showGenerateResumeModal()
            reGeneratePDF(order_data.id)
            setTimeout(function () {
                window.location.href = `${siteDomain}/dashboard`
                hideGenerateResumeModal()
            }, 5000);
        } else {
            history.push(`/resume-builder/buy`)
        }
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    async openModal() {
        const {experience} = this.props;
        let latest_experience = ''
        let latest_end_date = 'None'
        for (let exp of experience.list) {
            if (exp.is_working) {
                latest_experience = exp.job_profile
                break
            } else if (latest_end_date === 'None') {
                latest_end_date = exp.end_date
                latest_experience = exp.job_profile
            } else {
                if (latest_end_date < exp.end_date) {
                    latest_end_date = exp.end_date
                    latest_experience = exp.job_profile
                }

            }

        }

        let label = (latest_experience && latest_experience.label) || ''
        await this.props.fetchJobTitles(label, 'summary')
        this.setState({modal_status: true})
    }

    closeModal(suggestions) {
        const {extra_info, upateSummaryWithSuggestion} = this.props
        if (Object.keys(suggestions).length) {
            let suggestionsList = (extra_info ? extra_info + "\n" : '');
            Object.keys(suggestions).map((el, index) => {
                suggestionsList += suggestions[el] + (index + 1 === Object.keys(suggestions).length ? "" : '\n')
                return el;
            })
            upateSummaryWithSuggestion(suggestionsList)
        }
        this.setState({modal_status: false})
    }


    shouldComponentUpdate(nextProps, nextState, nextContext) {
        return true;
    }


    render() {
        const {extra_info, ui: {suggestions}, handleInputValue, handleSubmit, showAlertModal, history, isEditable, editHeading, saveTitle, entityName, nextEntity, personalInfo: {order_data}} = this.props;
        const {modal_status} = this.state;
        return (
            <div>
                <SuggestionModal label={'Summary'} length={extra_info.length} maxLength="1000"
                                 modal_status={modal_status} closeModal={this.closeModal} suggestions={suggestions}/>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-summary1"/></span>
                    {!!(!isEditable) ?
                        <h2>{entityName}
                        </h2> :
                        <React.Fragment>
                            <input autoFocus type="text" name="" defaultValue={entityName}
                                   onChange={(event) => handleInputValue(event.target.value || entityName)}
                                   maxLength="20"/>
                            <span onClick={(event) => saveTitle(event, 6)} className="icon-tick"/>
                        </React.Fragment>
                    }
                    <span onClick={() => editHeading()}
                          className={!!(!isEditable) ? "icon-edit " + styles['icon-summary__cursor'] : ''}/>
                </section>
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                    <section className="right-sidebar-scroll p3p">
                        <div className={styles['summary-box']}>
                            <h3>Summary</h3>
                            <Field
                                noIcon={true}
                                component={renderTextArea} type={"textarea"} name="extra_info" maxLength={"1000"}
                                className="summary-box--summary-txt" rows="10" value={extra_info}/>
                        </div>
                        <span className="add-suggested mt-15" onClick={() => {
                            this.openModal()
                        }}>Add suggested summary</span>

                    </section>


                    <SavePreviewButtons
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                    />
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
        ui: state.ui,
        experience: state.experience,
        extra_info: (state.form && state.form.summary && state.form.summary.values && state.form.summary.values.extra_info) || ''
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "upateSummaryWithSuggestion": (data) => {
            return dispatch(actions.upateSummaryWithSuggestion(data))
        },
        "fetchUserExperience": () => {
            return dispatch(fetchUserExperience())
        },
        "fetchJobTitles": (inputValue, suggestionType) => {
            if (inputValue.length < 3) return new Promise(res => res([]));
            return new Promise((res, rej) => {
                return dispatch(fetchJobTitles({inputValue, suggestionType, res, rej}))
            })
        },
        "onSubmit": (personalDetails, storeInformation) => {
            const {gender, extracurricular} = personalDetails;
            const {entity_preference_data} = storeInformation;
            personalDetails = {
                ...personalDetails,
                ...{
                    'gender': (gender && gender['value']) || '',
                    'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).filter(el => el !== undefined).map(el => el.value).join(',') : '',
                    'entity_preference_data': (entity_preference_data || []).map(el => el)
                }
            };

            personalDetails = {
                ...personalDetails,
                ...{
                    'extracurricular': personalDetails.extracurricular instanceof Array && personalDetails.extracurricular.length ?
                        '' : personalDetails.extracurricular

                }
            };

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
