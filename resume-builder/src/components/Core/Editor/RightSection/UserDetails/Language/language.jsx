import React, {Component} from 'react';
import './language.scss'
import {Field, reduxForm, FieldArray, arrayPush} from "redux-form";
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

/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.state = {
            currentAccordion: 0
        }
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
    }


    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=award')
    }

    handleAccordionClick(value) {
        console.log('0----', value);
    }

    render() {
        const {handleSubmit, language: {list}} = this.props;
        const renderMembers = ({fields, list, meta: {error, submitField}}) => {
            return (

                <ul>
                    <li>
                        <section className="head-section">
                            <span className="icon-box"><i className="icon-languages1"></i></span>
                            <h2>Languages</h2>
                            <span className="icon-edit icon-language__cursor"></span>
                            <button onClick={() => fields.push({
                                "candidate_id": '',
                                "id": '',
                                "name": '',
                                "proficiency": 5
                            })}
                                    type={'button'}
                                    className="add-button add-button__right">Add new
                            </button>
                        </section>
                    </li>
                    <section className="right-sidebar-scroll">
                        <Accordion onChange={this.handleAccordionClick}>
                            {fields.map((member, index) => {
                                    return (
                                        <li key={index}>
                                            <AccordionItem>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{list[index] && list[index].name || 'Language'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span className="icon-delete mr-15"></span>
                                                                <span className="icon-ascend mr-5"></span>
                                                                <span className="icon-descend"></span>
                                                            </div>
                                                        </div>
                                                    </AccordionItemButton>
                                                </AccordionItemHeading>
                                                <AccordionItemPanel>
                                                    <section className="info-section">
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
                                                            <Field component={'input'} name={`${member}.id`} type={'text'}
                                                                   hidden={true}/>

                                                        </div>
                                                    </section>
                                                </AccordionItemPanel>
                                            </AccordionItem>
                                        </li>
                                    )
                                }
                            )}
                        </Accordion>

                    </section>
                </ul>
            )
        };
        return (
            <div>

                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" list={list} component={renderMembers}/>
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
    enableReinitialize: true
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
            console.log('sybmitt', userLanguage);
            const {proficiency} = userLanguage;
            userLanguage = {
                ...userLanguage,
                ...{
                    proficiency: (proficiency && proficiency.value) || 5
                }
            }
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserLanguage({userLanguage, resolve, reject}));
            })
        },
        "fetchUserLanguage": () => {
            return dispatch(actions.fetchUserLanguage())
        },
        pushArray: arrayPush

    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
