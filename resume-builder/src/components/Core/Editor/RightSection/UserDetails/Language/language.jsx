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

import validate from '../../../../../FormHandler/languageValidation'
/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';

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

    async handleSubmit(values) {
        const {list} = values;
        await this.props.onSubmit(list[list.length - 1]);
        this.props.history.push('/resume-builder/edit/?type=award')
    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation()
        console.log('donw pressed');
        fields.swap(index, index + 1);
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('up pressed');
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1)
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            }
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

        console.log('--accordion--', currentAccordion);
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
        const val = value.length > 0 ? value[0] : ''
        this.handleAccordionState(val, fields)
    }


    render() {
        const {handleSubmit, language: {list}} = this.props;
        const renderMembers = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                <div>
                    <section className="head-section">
                        <span className="icon-box"><i className="icon-languages1"></i></span>
                        <h2>Languages</h2>
                        <span className="icon-edit icon-language__cursor"></span>
                        <button onClick={this.handleAddition.bind(this, fields, error)}
                                type={'button'}
                                className="add-button add-button__right">Add new
                        </button>
                        {(touched || submitFailed) && error && <span>{error}</span>}
                    </section>
                    <section className="right-sidebar-scroll">
                        <ul>
                            <Accordion onChange={(value) => this.handleAccordionClick(value, fields, error)}
                                       allowZeroExpanded={true}
                                       preExpanded={[this.state.openedAccordion]}>
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
                                                                    onClick={(event) => this.deleteLanguage(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                        {index !== 0 &&
                                                                        <span
                                                                            onClick={(event) => this.changeOrderingUp(index, fields, event)}
                                                                            className="icon-ascend mr-5"/>
                                                                        }
                                                                        {
                                                                            index !== fields.length - 1 &&
                                                                            < span
                                                                                onClick={(event) => this.changeOrderingDown(index, fields, event)}
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
                                                                            <span className="icon-blank"></span>
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
        };
        return (
            <div>

                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderMembers}/>
                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>
            </div>
        )
    }
}


export const LanguageForm = reduxForm({
    form: 'Language',
    validate,
    enableReinitialize: true,

})(Language);


const mapStateToProps = (state) => {
    return {
        initialValues: state.language,
        language: state.language
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
            return dispatch(actions.handleLanguageSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
