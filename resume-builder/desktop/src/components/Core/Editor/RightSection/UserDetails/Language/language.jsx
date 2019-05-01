import React, {Component} from 'react';
import './language.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';

import validate from '../../../../../FormHandler/validations/language/validate'
/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';
import LoaderSection from "../../../../../Loader/loaderSection.jsx";

const LanguageRenderer = ({
                              fields,
                              loader,
                              meta: {touched, error, submitFailed},
                              deleteLanguage,
                              handleSubmit,
                              handleAddition,
                              handleAccordionState,
                              handleAccordionClick,
                              changeOrderingUp,
                              changeOrderingDown,
                              openedAccordion,
                              entity,
                              isEditable,
                              editHeading,
                              saveTitle,
                              entityName
                          }) => {
    let elem = null;

    return (
        <div>
            {/*{!!loader &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-languages1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-language__cursor" : ""}/>

                <button onClick={handleSubmit((values) => {
                    handleAddition(fields, error)
                })}
                        type={'button'}
                        className="add-button add-button__right">Add new
                </button>

            </section>
            <section className="right-sidebar-scroll">
                <ul>
                    <Accordion onChange={(value) => handleAccordionClick(value, fields, submitFailed)}
                               allowZeroExpanded={true}
                               preExpanded={[0,1,2,3,4,5,6,7,8,9,10]}>
                        {fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).name || 'Language'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteLanguage(index, fields, event)}
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
                                                        <fieldset className="width-half">
                                                            <label>Language name</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-language-gr"></span>
                                                                </div>
                                                                <Field component={renderField} type={"text"}
                                                                       name={`${member}.name`}
                                                                       className={"input-control"}/>
                                                            </div>
                                                        </fieldset>

                                                        <fieldset className="width-half">
                                                            <label>Language rating (out of 10)</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-rating"></span>
                                                                </div>
                                                                <Field name={`${member}.proficiency`}
                                                                       component={renderSelect}
                                                                       isMulti={false}
                                                                       options={[
                                                                           {value: 1, label: '1'},
                                                                           {value: 2, label: '2'},
                                                                           {value: 3, label: '3'},
                                                                           {value: 4, label: '4'},
                                                                           {value: 5, label: '5'},
                                                                           {value: 6, label: '6'},
                                                                           {value: 7, label: '7'},
                                                                           {value: 8, label: '8'},
                                                                           {value: 9, label: '9'},
                                                                           {value: 10, label: '10'}
                                                                       ]}/>
                                                            </div>
                                                        </fieldset>
                                                        <Field component={'input'} name={`${member}.id`}
                                                               type={'text'}
                                                               hidden={true}/>

                                                    </div>

                                                </AccordionItemPanel>
                                            </AccordionItem>
                                        </section>
                                    </li>
                                )
                            }
                        )}
                    </Accordion>
                </ul>
            </section>


        </div>
    )
}

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
        }
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }
    }

    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem])
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])
    }

    async handleAddition(fields, error) {
        const listLength = fields.length;
        // if (listLength) this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: fields.length
        })
    }


    deleteLanguage(index, fields, event) {
        event.stopPropagation();
        const language = fields.get(index);
        fields.remove(index);
        if (language && language.id) {
            this.props.removeLanguage(language.id)
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
        const {
            handleSubmit, ui: {loader}, isEditable,
            editHeading, saveTitle, entityName, nextEntity, handlePreview
        } = this.props;
        console.log('---', nextEntity);
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name="list"
                    loader={loader}
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAccordionState={this.handleAccordionState}
                    handleAddition={this.handleAddition}
                    deleteLanguage={this.deleteLanguage}
                    changeOrderingUp={this.changeOrderingUp}
                    changeOrderingDown={this.changeOrderingDown}
                    openedAccordion={this.state.openedAccordion}
                    component={LanguageRenderer}
                    saveTitle={(event) => saveTitle(event, 8)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type={'button'} onClick={handlePreview}>Preview</button>
                    <button className="orange-button" type={'submit'}>Save & Continue</button>
                </div>
            </form>
        )
    }
}


export const LanguageForm = reduxForm({
    form: 'Language',
    enableReinitialize: true,
    validate,


})(Language);


const mapStateToProps = (state) => {
    return {
        initialValues: state.language,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userLanguage) => {
            const {proficiency} = userLanguage;
            userLanguage = {
                ...userLanguage,
                ...{
                    proficiency: (proficiency && proficiency.value) || 5
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserLanguage({userLanguage, resolve, reject}));
            })
        },
        "fetchUserLanguage": () => {
            return dispatch(actions.fetchUserLanguage())
        },
        "removeLanguage": (languageId) => {
            return dispatch(actions.deleteLanguage(languageId))
        },

        "handleSwap": (listItems) => {
            listItems = (listItems || []).map(item => {
                const {proficiency} = item;
                if (!item['id']) delete item['id'];
                item = {
                    ...item,
                    ...{
                        proficiency: (proficiency && proficiency.value) || 5

                    }
                }
                return item;
            })
            return dispatch(actions.handleLanguageSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
