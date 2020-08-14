import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import { connect } from "react-redux";
import { ReferenceRenderer } from "./referenceRenderer";
import validate from '../../../../../FormHandler/validations/reference/validate'
import { scroller } from "react-scroll/modules";
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import propTypes from 'prop-types';

class Reference extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteReference = this.deleteReference.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false
        };
        this.props.currentForm('reference');

    }

    async handleSubmit(values, entityLink) {
        const { generateResumeAlert, bulkUpdateOrCreate, history } = this.props

        const { list } = values;
        if (list.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;

            list.map(el => {
                if (!el.reference_name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateOrCreate(list);
            }
            
        }

        this.setState({
            submit: true
        })
        
        if (entityLink) history.push(entityLink);
        else {
            generateResumeAlert()
        }
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    async componentDidUpdate(prevProps) {
        const { ui: { previewClicked }, previewButtonClicked, history } = this.props;
        if (previewClicked !== prevProps.ui.previewClicked && previewClicked) {
            await this.updateInfoBeforeLoss()
            this.setState({ submit: true })
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }

    async updateInfoBeforeLoss() {
        let { initialValues, formData: { reference: { values, syncErrors } } } = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues) !== JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
    }

    componentDidMount() {
        this.props.fetchUserReference()
    }


    handleAddition(fields, error) {
        const listLength = fields.length;
        fields.push({
            "candidate_id": '',
            "id": '',
            "reference_name": '',
            "reference_designation": '',
            "about_user": "",
            order: listLength
        })

        scroller.scrollTo(`reference${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 200,
            containerId: 'reference'
        })
        this.props.eventClicked({
            'action': 'AddNew',
            'label': 'References'
        })
    }

    deleteReference(index, fields, event) {
        event.stopPropagation();
        const reference = fields.get(index);
        fields.remove(index);
        if (reference && reference.id) {
            this.props.removeReference(reference.id)
        }


    }


    handleAccordionClick(value, ) {
        this.setState({ active: value })
    }


    render() {
        const {
            handleSubmit, userInfo: { order_data }, ui: { loader }, isEditable, changeOrderingDown, eventClicked,
            editHeading, saveTitle, entityName, nextEntity, showAlertModal, history, handleInputValue, changeOrderingUp,
            showAlertMessage
        } = this.props;
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name={"list"}
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAddition={this.handleAddition}
                    deleteReference={this.deleteReference}
                    changeOrderingUp={changeOrderingUp}
                    changeOrderingDown={changeOrderingDown}
                    loader={loader}
                    component={ReferenceRenderer}
                    saveTitle={(event) => saveTitle(event, 10)}
                    editHeading={() => editHeading(10)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}
                    handleInputValue={handleInputValue}
                    showAlertMessage={showAlertMessage}
                />

                <SavePreviewButtons
                    showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'References'}
                    nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
                />
            </form>
        )
    }
}

Reference.propTypes = {
    currentForm: propTypes.func,
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
    bulkUpdateOrCreate: propTypes.func,
    generateResumeAlert: propTypes.func,
    previewButtonClicked: propTypes.func,
    previewClicked: propTypes.func,
    initialValues: propTypes.object,
    formData: propTypes.object,
    bulkUpdateOrCreate: propTypes.func,
    fetchUserReference: propTypes.func,
    eventClicked: propTypes.func,
    removeReference: propTypes.func,
    handleSubmit: propTypes.func,
    userInfo: propTypes.shape({
        active_subscription: propTypes.bool,
        candidate_id: propTypes.string,
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        free_resume_downloads: propTypes.number,
        gender: propTypes.object,
        id: propTypes.number,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
        selected_template: propTypes.string,
    }),
    ui: propTypes.shape({
        alertModal: propTypes.bool,
        alertType: propTypes.string,
        formName: propTypes.string,
        generateResumeModal: propTypes.bool,
        helpModal: propTypes.bool,
        loader: propTypes.bool,
        loginModal: propTypes.bool,
        modal: propTypes.bool,
        previewClicked: propTypes.bool,
        select_template_modal: propTypes.bool,
        showMoreSection: propTypes.bool,
        successLogin: propTypes.bool,
        suggestionModal: propTypes.bool,
        suggestionType: propTypes.string,
        suggestions: propTypes.array,
    }),
    saveTitle: propTypes.func,
    editHeading: propTypes.func,
    isEditable: propTypes.bool,
    entityName: propTypes.string,
    handleInputValue: propTypes.func,
    showAlertModal: propTypes.func,
    changeOrderingDown: propTypes.func,
    changeOrderingUp: propTypes.func,
    showAlertMessage: propTypes.func,
}

export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'reference', -100),
    validate
})(Reference);


const mapStateToProps = (state) => {
    return {
        initialValues: state.reference,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userReference) => {
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserReference({ userReference, resolve, reject }));
            })
        },
        "fetchUserReference": () => {
            return dispatch(actions.fetchUserReference())
        },
        "removeReference": (referenceId) => {
            return dispatch(actions.deleteReference(referenceId))
        },

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userReference, index) => {
                if (!userReference['id']) delete userReference['id'];
                userReference = {
                    ...userReference,
                    ...{
                        order: index
                    }
                }
                return userReference;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserReference({ list: listItems, resolve, reject }))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
