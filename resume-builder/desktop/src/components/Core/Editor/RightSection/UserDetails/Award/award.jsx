import React, {Component} from 'react';
import {FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/award/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/award/validate";
import {AwardRenderer} from "./awardRenderer";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import {scroller} from "react-scroll/modules";
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import propTypes from 'prop-types';

class Award extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteAward = this.deleteAward.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false

        }
        this.props.currentForm('award');
    }

    componentDidMount() {
        this.props.fetchUserAward()
    }

    async componentDidUpdate(prevProps){
        const {ui:{previewClicked},previewButtonClicked,history} = this.props;
        if(previewClicked !== prevProps.ui.previewClicked && previewClicked){
            await this.updateInfoBeforeLoss()
            this.setState({submit:true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }

    async updateInfoBeforeLoss(){
        let { initialValues, formData: {award: {values, syncErrors}}} = this.props;
        let error = false;
        ((syncErrors && syncErrors['list']) || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)));
        if (!error && !this.state.submit && JSON.stringify(initialValues)!==JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    async handleSubmit(values, entityLink) {
         const {generateResumeAlert,bulkUpdateOrCreate,history} = this.props
        const {list} = values;
        if (list.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            
            list.map(el => {
                if(! el.title){
                    skipApiCall = true;
                }
                return; 
            })

            if(!skipApiCall){
                await bulkUpdateOrCreate(list);
            }
        }

        this.setState({
            submit: true
        })

        if (entityLink) history.push(entityLink);
            else{
                generateResumeAlert()
            }
    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            order: listLength
        })

        scroller.scrollTo(`award${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 200,
            containerId: 'award'
        })
        this.props.eventClicked({
            'action':'AddNew',
            'label':'Awards'
        })
    }

    deleteAward(index, fields, event) {
        event.stopPropagation();
        const award = fields.get(index);
        fields.remove(index);
        if (award && award.id) {
            this.props.removeAward(award.id)
        }
    }

    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit,userInfo:{order_data}, ui: {loader}, saveTitle, editHeading,eventClicked,
            isEditable, entityName, handleInputValue, nextEntity, showAlertModal,history, changeOrderingDown, changeOrderingUp, showAlertMessage
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name="list"
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteAward={this.deleteAward}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={AwardRenderer}
                            saveTitle={(event) => saveTitle(event, 7)}
                            editHeading={() => editHeading(7)}
                            entityName={entityName}
                            isEditable={isEditable}
                            handleInputValue={handleInputValue}
                            expanded={this.state.active}
                            showAlertMessage={showAlertMessage}
                />
                <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'Awards'}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
                    />

            </form>
        )
    }
}

Award.propTypes = {
    currentForm: propTypes.func,
    fetchUserAward: propTypes.func,
    ui: propTypes.shape({
        alertModal: propTypes.bool,
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
    previewButtonClicked: propTypes.func,
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
    initialValues: propTypes.object,
    formData: propTypes.object,
    bulkUpdateOrCreate: propTypes.func,
    generateResumeAlert: propTypes.func,
    eventClicked: propTypes.func,
    removeAward: propTypes.func,
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

export const AwardForm = reduxForm({
    form: 'award',
    validate,
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'award', -100),
})(Award);


const mapStateToProps = (state) => {
    return {
        initialValues: state.award,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userAward) => {
            const {date} = userAward;

            userAward = {
                ...userAward,
                ...{
                    date: (date && moment(date).format('YYYY-MM-DD')) || '',
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserAward({userAward, resolve, reject}));
            })
        },
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
        "removeAward": (awardId) => {

            return dispatch(actions.deleteAward(awardId))
        },

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userAward, index) => {
                const {date} = userAward;
                if (!userAward['id']) delete userAward['id'];
                userAward = {
                    ...userAward,
                    ...{
                        date: (date && date.value && Number(date.value)) || null,
                        order: index
                    }
                };
                return userAward;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserAward({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);
