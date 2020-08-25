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
        this.props.sendTrackingInfo('right_section_add',1)
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
        this.props.sendTrackingInfo('right_section_delete',1)
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
