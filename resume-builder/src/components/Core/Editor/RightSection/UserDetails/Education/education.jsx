import React, {Component} from 'react';
import './education.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {required} from "../../../../../FormHandler/formValidations"
import * as actions from "../../../../../../store/education/actions";
import {connect} from "react-redux";
import moment from "moment";
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';

import validate from '../../../../../FormHandler/educationValidation'

class Education extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteEducation = this.deleteEducation.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,

        }
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=skill')
    }

    componentDidMount() {
        this.props.fetchUserEducation()
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

    deleteEducation(index, fields, event) {
        event.stopPropagation();
        const education = fields.get(index);
        fields.remove(index);
        if (education && education.id) {
            this.props.removeEducation(education.id)
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
        const {handleSubmit, education} = this.props;
        const renderEducation = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                <div>
                    <section className="head-section">
                        <span className="icon-box"><i className="icon-languages1"></i></span>
                        <h2>Education</h2>
                        <span className="icon-edit icon-language__cursor"></span>
                        <button onClick={this.handleAddition.bind(this, fields, error)}
                                type={'button'}
                                className="add-button add-button__right">Add new
                        </button>
                        {(touched || submitFailed) && error && <span>{error}</span>}

                    </section>
                    <section className="right-sidebar-scroll">
                        <ul>
                            <Accordion>
                                {
                                    fields.map((member, index) => {
                                        return (
                                            <li key={'index'}>
                                                <section className="info-section">
                                                    <AccordionItem uuid={index}>
                                                        <AccordionItemHeading>
                                                            <AccordionItemButton>
                                                                <div className="flex-container">
                                                                    <h3 className="add-section-heading">{fields.get(index).name || 'Education'}</h3>
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
                                                                <fieldset>
                                                                    <label>Institution Name </label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-company"></span>
                                                                        </div>
                                                                        <Field component={renderField} type={"text"}
                                                                               name={`${member}.institution_name`}/>
                                                                    </div>
                                                                </fieldset>
                                                                <fieldset>
                                                                    <label>Specialization</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-designation"></span>
                                                                        </div>
                                                                        <Field component={renderField} type={"text"}

                                                                               name={`${member}.specialization`}/>
                                                                    </div>
                                                                </fieldset>
                                                            </div>

                                                            <div className="flex-container">
                                                                <fieldset>
                                                                    <label>Date from</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-date"></span>
                                                                        </div>
                                                                        <Field component={datepicker} type={"date"}

                                                                               name={`${member}.start_date`}
                                                                               className="input-control"/>
                                                                    </div>
                                                                </fieldset>
                                                                <fieldset>
                                                                    <label>Date to</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-date"></span>
                                                                        </div>
                                                                        <Field component={datepicker}
                                                                               type={"date"}
                                                                               name={`${member}.end_date`}
                                                                               className="input-control"/>

                                                                    </div>
                                                                    <span className="till-today">
                                    <Field type="radio" name={`${member}.is_pursuing`} component={'input'}
                                           value={education.is_pursuing}/>
                                    Till Today
                                </span>
                                                                </fieldset>
                                                            </div>

                                                            <div className="flex-container">

                                                                <fieldset className="custom">
                                                                    <label>Course Type</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-blank"></span>
                                                                        </div>
                                                                        <Field component={renderSelect} type={"text"}
                                                                               name={`${member}.course_type`}
                                                                               options={[
                                                                                   {value: 'FT', label: 'FULL TIME'},
                                                                                   {value: 'PT', label: 'PART TIME'},
                                                                               ]}
                                                                               className="input-control"/>
                                                                    </div>
                                                                </fieldset>
                                                                <fieldset>
                                                                    <label>Percentage/CGPA</label>
                                                                    <div className="input-group">
                                                                        <div className="input-group--input-group-icon">
                                                                            <span className="icon-blank"></span>
                                                                        </div>
                                                                        <Field component={renderField} type={"text"}
                                                                               name={`${member}.percentage_cgpa`}
                                                                               className="input-control"/>
                                                                    </div>
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
                </div>
            )
        }
        return (
            <div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name={'list'} component={renderEducation}/>
                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>

            </div>
        )
    }
}


export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true,
    validate
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education,
        education: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userEducation) => {
            const {start_date, end_date, course_type} = userEducation;

            userEducation = {
                ...userEducation,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                    course_type: course_type && course_type.value
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserEducation({userEducation, resolve, reject}));
            })
        },
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
        "removeEducation": (educationId) => {
            return dispatch(actions.deleteEducation(educationId))
        },

        "handleSwap": (listItems) => {
            return dispatch(actions.handleEducationSwap({list: listItems}))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
