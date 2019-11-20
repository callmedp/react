import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {ReferenceRenderer} from "./referenceRenderer";
import validate from '../../../../../FormHandler/validations/reference/validate'
import {scroller} from "react-scroll/modules";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';


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
         const {generateResumeAlert,bulkUpdateOrCreate,history} = this.props

        const {list} = values;
        if (list.length) {
            await bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) history.push(entityLink);
            else{
                generateResumeAlert()
            }
        }
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
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
        let { initialValues, formData: {reference: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues)!==JSON.stringify(values)) await this.props.bulkUpdateOrCreate(values && values['list'])
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
            'action':'AddNew',
            'label':'References'
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


    handleAccordionClick(value,) {
        this.setState({active: value})
    }


    render() {
        const {
            handleSubmit,userInfo:{order_data}, ui: {loader}, isEditable, changeOrderingDown,eventClicked,
            editHeading, saveTitle, entityName, nextEntity, showAlertModal,history, handleInputValue,changeOrderingUp
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


                />

                <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'References'}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
                    />
            </form>
        )
    }
}


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'reference',-100),
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
                return dispatch(actions.updateUserReference({userReference, resolve, reject}));
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
                return dispatch(actions.bulkUpdateOrCreateUserReference({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
