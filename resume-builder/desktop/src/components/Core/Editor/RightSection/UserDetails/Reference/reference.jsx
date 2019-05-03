import React, {Component} from 'react';
import './reference.scss'
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {ReferenceRenderer} from "./referenceRenderer";
import validate from '../../../../../FormHandler/validations/reference/validate'


class Reference extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteReference = this.deleteReference.bind(this);

        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        }
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }
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
            handleSubmit, ui: {loader}, isEditable, changeOrderingDown,
            editHeading, saveTitle, entityName, nextEntity, handlePreview, changeOrderingUp
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
                    saveTitle={(event) => saveTitle(event, 9)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}

                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type={'button'} onClick={handlePreview}>Preview</button>
                    <button className="orange-button" type={'submit'}>Save & Continue</button>
                </div>
            </form>
        )
    }
}


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true,
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
            listItems = (listItems || []).map(userReference => {
                if (!userReference['id']) delete userReference['id'];
                return userReference;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserReference({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
