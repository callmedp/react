import React, {Component} from 'react';
import './education.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
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

import validate from '../../../../../FormHandler/validations/education/validate';
import LoaderSection from "../../../../../Loader/loaderSection.jsx";
import {animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'


const EducationRenderer = ({
                               fields,
                               loader,
                               meta: {touched, error, submitFailed},
                               deleteEducation,
                               handleAddition,
                               handleSubmit,
                               handleAccordionState,
                               handleAccordionClick,
                               changeOrderingUp,
                               changeOrderingDown,
                               openedAccordion,
                               editHeading,
                               saveTitle,
                               isEditable,
                               entityName
                           }) => {
    let elem = null;
    return (
        <div className="pr">
            {/*{<LoaderSection/>}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-education1"></i></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}>{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-education__cursor" : ''}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className="add-button add-button__right">Add new
                </button>


            </section>


            <section className="right-sidebar-scroll">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value, fields, error)}
                        allowZeroExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                    >
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index} id={`education${index}`}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).specialization || 'Education'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteEducation(index, fields, event)}
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
                                    <Field type="checkbox" name={`${member}.is_pursuing`} component={'input'}
                                           checked={`${member}.is_pursuing` === 'true'}/>
                                    Till Today
                                </span>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">

                                                        <fieldset className="custom">
                                                            <label>Course Type</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-course-type"></span>
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
                                                                    <span className="icon-percentage"></span>
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

class Education extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteEducation = this.deleteEducation.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
            isEditable: false
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
        this.props.fetchUserEducation()
    }

    handleAddition(fields, error, event) {
        const listLength = fields.length;
        // if (listLength) this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "specialization": '',
            "institution_name": '',
            "course_type": '',
            "start_date": '',
            "percentage_cgpa": '',
            "end_date": '',
            "is_pursuing": false,
            order: fields.length
        })
        console.log('-fields--', fields.length);

        scroller.scrollTo(`education1`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 1000
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
            handleSubmit, ui: {loader}, saveTitle, isEditable,
            editHeading, entityName, nextEntity, handlePreview, changeOrderingUp
            , changeOrderingDown
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={'list'}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAccordionState={this.handleAccordionState}
                            handleAddition={this.handleAddition}
                            deleteEducation={this.deleteEducation}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            openedAccordion={this.state.openedAccordion}
                            component={EducationRenderer}
                            saveTitle={(event) => saveTitle(event, 1)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" onClick={handlePreview}>Preview</button>
                    <button className="orange-button" type={'submit'}>Save & Continue</button>
                </div>

            </form>
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
        ui: state.ui,
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

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map(userEducation => {
                    const {start_date, end_date, course_type} = userEducation;
                    if (!userEducation['id']) delete userEducation['id'];
                    userEducation = {
                        ...userEducation,
                        ...{
                            start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                            end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                            course_type: course_type && course_type.value
                        }
                    };
                    return userEducation;
                }
            );
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserEducation({list: listItems, resolve, reject}))
            })

        },

        "handleSwap":
            (listItems) => {
                listItems = (listItems || []).map(userEducation => {
                        const {start_date, end_date, course_type} = userEducation;
                        if (!userEducation['id']) delete userEducation['id'];
                        userEducation = {
                            ...userEducation,
                            ...{
                                start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                                end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                                course_type: course_type && course_type.value
                            }
                        };
                        return userEducation;
                    }
                );
                return dispatch(actions.handleEducationSwap({list: listItems}))
            }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
