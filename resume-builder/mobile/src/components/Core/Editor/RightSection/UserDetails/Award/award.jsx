import React, { Component } from 'react';
import { reduxForm, FieldArray } from "redux-form";
import * as actions from "../../.../../../../../../store/award/actions";
import { connect } from "react-redux";
import validate from "../../../../../FormHandler/validtaions/award/validate"
import PreviewModal from "../../../Preview/changeTemplateModal";
import renderAwards from "./renderAwards"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError"
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import Subscribe from "../../../RightSection/subscribe";


class Award extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.deleteAward = this.deleteAward.bind(this);
        this.state = {
            'editHeading': false,
            'heading': '',
            'submit': false
        }
        this.editHeadingClick = this.editHeadingClick.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserAward()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[6].entity_text })
        }
    }

    async updateInfoBeforeLoss() {
        if (!this.state.submit) {
            const { initialValues } = this.props
            const form_data = this.props.info.form.award;
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
                await this.props.bulkUpdateUserAward(values.list)
            }
        }
    }

    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }


    async handleSubmit(values) {
        values = this.state.fields ? this.state.fields : values.list
        let { sidenav: { listOfLinks, currentLinkPos }, bulkUpdateUserAward, updateCurrentLinkPos, history,
            generateResumeAlert } = this.props;
        currentLinkPos++;
        if (values.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;

            values.map(el => {
                if (!el.title) {
                    skipApiCall = true;
                }
                return;
            })
            if (!skipApiCall) {
                await bulkUpdateUserAward(values);
            }
        }
        this.setState({ submit: true });
        if (currentLinkPos === listOfLinks.length) {
            currentLinkPos = 0
            generateResumeAlert()
        }
        else {
            updateCurrentLinkPos({ currentLinkPos })
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
    }

    deleteAward(index, fields, event) {
        this.props.sendTrackingInfo('right_section_delete',1)
        event.stopPropagation();
        const award = fields.get(index);
        fields.remove(index);
        if (award && award.id) {
            this.props.removeAward(award.id)
        }
    }


    editHeadingClick() {
        this.setState({ editHeading: true })
        this.props.sendTrackingInfo('right_section_edit',1)
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[6].entity_text })
        }
    }

    render() {
        const { handleSubmit, submitting, history, personalInfo: { order_data, entity_preference_data }, changeOrderingUp, changeOrderingDown, headingChange, updateAlertModalStatus, eventClicked, showAlertMessage } = this.props;
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { editHeading, heading } = this.state;

        return (
            <div className="buildResume">
                <PreviewModal {...this.props} />
                <Subscribe {...this.props} />
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values))}>
                    <FieldArray name="list"
                        handleSubmit={handleSubmit}
                        handleAddition={this.props.handleAddition}
                        deleteAward={this.deleteAward}
                        changeOrderingUp={changeOrderingUp}
                        changeOrderingDown={changeOrderingDown}
                        eventClicked={eventClicked}
                        component={renderAwards}
                        headingChange={headingChange}
                        editHeading={editHeading}
                        editHeadingClick={this.editHeadingClick}
                        entity_preference_data={entity_preference_data}
                        context={this}
                        heading={heading}
                        showAlertMessage={showAlertMessage}
                    />
                    <ul className="form">
                        <li className="form__group">
                            <BottomCTC disabled={submitting} context={this} history={history} updateAlertModalStatus={updateAlertModalStatus}
                                length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                                order_data={order_data} eventClicked={eventClicked} form_name={'Awards'} />
                        </li>
                    </ul>
                </form>
            </div>

        )
    }
}

export const AwardForm = reduxForm({
    form: 'award',
    validate,
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'award', -100),
})(Award);


const mapStateToProps = (state) => {
    return {
        initialValues: state.award,
        award: state.award,
        info123: state
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
        "removeAward": (awardId) => {
            return dispatch(actions.deleteAward(awardId))
        },
        "bulkUpdateUserAward": (listItems) => {
            listItems = (listItems || []).map((userAward, index) => {
                const { date } = userAward;
                if (!userAward['id']) delete userAward['id'];
                userAward = {
                    ...userAward,
                    ...{
                        date: parseInt(date)
                    }
                };
                return userAward;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateUserAward({ list: listItems, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);