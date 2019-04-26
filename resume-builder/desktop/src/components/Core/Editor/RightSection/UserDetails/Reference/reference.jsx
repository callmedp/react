import React, {Component} from 'react';
import './reference.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';

import validate from '../../../../../FormHandler/validations/referenceValidation'
import Loader from "../../../../../Loader/loader.jsx";


const ReferenceRenderer = ({
                               fields,
                               loader,
                               meta: {touched, error, submitFailed},
                               deleteReference,
                               handleAddition,
                               handleAccordionState,
                               handleAccordionClick,
                               changeOrderingUp,
                               changeOrderingDown,
                               openedAccordion,
                           }) => {
    return (
        <div>
            {!!loader &&
            <Loader/>
            }
            <section className="head-section">
                <span className="icon-box"><i className="icon-references1"/></span>
                <h2 contenteditable="true">References</h2>
                <span className="icon-edit icon-edit__cursor"></span>

                <button
                    onClick={() => handleAddition(fields)}
                    type={'button'}
                    className="add-button add-button__right">Add new
                </button>


                {/*{(touched || submitFailed) && error && <span>{error}</span>}*/}
            </section>
            <section>
                <section className="right-sidebar-scroll">
                    <ul>
                        <Accordion
                            onChange={(value) => handleAccordionClick(value, fields)}
                            allowZeroExpanded={true}
                            preExpanded={[openedAccordion]}>
                            {
                                fields.map((member, index) => {
                                    return (
                                        <li key={index}>
                                            <section className="info-section">
                                                <AccordionItem uuid={index}>
                                                    <AccordionItemHeading>
                                                        <AccordionItemButton>
                                                            <div className="flex-container">
                                                                <h3 className="add-section-heading">{fields.get(index).reference_name || 'Reference'}</h3>
                                                                <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteReference(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                    {index !== 0 &&
                                                                    <span
                                                                        onClick={(event) => changeOrderingUp(index, fields, event)}
                                                                        className="icon-ascend mr-5"/>
                                                                    }
                                                                    {
                                                                        index !== fields.length - 1 &&
                                                                        < span
                                                                            onClick={(event) => changeOrderingDown(index, fields, event)}
                                                                            className="icon-descend"/>
                                                                    }
                                                                </div>
                                                            </div>
                                                        </AccordionItemButton>
                                                    </AccordionItemHeading>
                                                    <AccordionItemPanel>

                                                        <div className="flex-container">
                                                            <fieldset className="error">
                                                                <label>Reference name</label>
                                                                <div className="input-group">
                                                                    <div
                                                                        className="input-group--input-group-icon">
                                                                                <span
                                                                                    className="icon-refrences-gr"/>
                                                                    </div>
                                                                    <Field component={renderField} type={"text"}
                                                                           name={`${member}.reference_name`}
                                                                           className={"input-control"}
                                                                    />
                                                                </div>
                                                            </fieldset>
                                                            <fieldset>
                                                                <label>Designation</label>
                                                                <div className="input-group">
                                                                    <div
                                                                        className="input-group--input-group-icon">
                                                                                <span
                                                                                    className="icon-designation"/>
                                                                    </div>
                                                                    <Field component={renderField} type={"text"}
                                                                           name={`${member}.reference_designation`}
                                                                           className={"input-control"}
                                                                    />
                                                                </div>
                                                            </fieldset>
                                                        </div>

                                                        <div className="flex-container">
                                                            <fieldset>
                                                                <label>Description</label>
                                                                <Field component={renderTextArea}
                                                                       type={"textarea"}
                                                                       name={`${member}.about_candidate`}/>
                                                            </fieldset>
                                                        </div>

                                                    </AccordionItemPanel>
                                                </AccordionItem>
                                            </section>
                                        </li>
                                    )
                                })
                            }
                        </Accordion>
                    </ul>
                </section>
            </section>

        </div>

    )

}

class Reference extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteReference = this.deleteReference.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
        }
    }

    async handleSubmit(values) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
        }
    }

    componentDidMount() {
        this.props.fetchUserReference()
    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        console.log('donw pressed');
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem]);
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('up pressed');
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        if (listLength) this.handleAccordionState(listLength, fields);
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


    handleAccordionState(val, fields) {
        const {currentAccordion} = this.state;

        if (currentAccordion !== '') {

            this.props.onSubmit(fields.get(currentAccordion))
        }

        this.setState((state) => ({
            previousAccordion: state.currentAccordion,
            openedAccordion: val,
            currentAccordion: val
        }))
    }

    handleAccordionClick(value, fields) {
        const val = value.length > 0 ? value[0] : '';
        this.handleAccordionState(val, fields)
    }


    render() {
        const {handleSubmit, ui: {loader}} = this.props;
        return (
            <form onSubmit={handleSubmit(this.handleSubmit)}>
                <FieldArray
                    name={"list"}
                    handleSubmit={this.handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAccordionState={this.handleAccordionState}
                    handleAddition={this.handleAddition}
                    deleteReference={this.deleteReference}
                    changeOrderingUp={this.changeOrderingUp}
                    changeOrderingDown={this.changeOrderingDown}
                    openedAccordion={this.state.openedAccordion}
                    loader={loader}
                    component={ReferenceRenderer}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
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

        "handleSwap": (listItems) => {
            listItems = (listItems || []).map(userReference => {
                if (!userReference['id']) delete userReference['id'];
                return userReference;
            })
            return dispatch(actions.handleReferenceSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
