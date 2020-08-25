import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import { connect } from "react-redux";
import renderReferences from "./renderReference"
import validate from "../../../../../FormHandler/validtaions/reference/validate"
import PreviewModal from "../../../Preview/changeTemplateModal";
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from '../../../RightSection/subscribe';

class References extends Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteReference = this.deleteReference.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserReference, generateResumeAlert, updateCurrentLinkPos,
            history } = this.props
        currentLinkPos++

        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;

            values.map(el => {
                if (!el.reference_name) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserReference(values);
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
            const form_data = this.props.info.form.reference;
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
                await this.props.bulkUpdateUserReference(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    componentDidMount() {
        this.props.fetchUserReference()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[9].entity_text })
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[9].entity_text })
        }
    }

    editHeadingClick() {
        this.setState({ editHeading: true })
        this.props.sendTrackingInfo('right_section_edit',1)
    }

    deleteReference(index, fields, event) {
        event.stopPropagation();
        const reference = fields.get(index);
        fields.remove(index);
        if (reference && reference.id) {
            this.props.removeReference(reference.id)
        }


    }

    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { updateAlertModalStatus, handleSubmit, history, personalInfo: { order_data, entity_preference_data },
            headingChange, submitting, changeOrderingUp, changeOrderingDown, eventClicked, showAlertMessage
        } = this.props;
        const { editHeading, heading } = this.state;
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props} />
                    <Subscribe {...this.props} />
                    <FieldArray name={"list"}
                        handleSubmit={handleSubmit}
                        handleAddition={this.props.handleAddition}
                        deleteReference={this.deleteReference}
                        changeOrderingUp={changeOrderingUp}
                        changeOrderingDown={changeOrderingDown}
                        eventClicked={eventClicked}
                        component={renderReferences}
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
                                order_data={order_data} eventClicked={eventClicked} form_name={'References'} />
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'references', -100),
    validate
})(References);


const mapStateToProps = (state) => {
    return {
        initialValues: state.reference,
        reference: state.reference
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

        "bulkUpdateUserReference": (listItems) => {
            listItems = (listItems || []).map(userReference => {
                if (!userReference['id']) delete userReference['id'];
                return userReference;
            })
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserReference({ list: listItems, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
