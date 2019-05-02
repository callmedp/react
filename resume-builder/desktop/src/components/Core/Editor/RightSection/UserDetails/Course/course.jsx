import React, {Component} from 'react';
import './course.scss'
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";
import validate from "../../../../../FormHandler/validations/course/validate"
import moment from "moment";
import Loader from "../../../../../Loader/loaderSection.jsx";

import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';


const CourseRenderer = ({
                            fields,
                            loader,
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            deleteCourse,
                            handleAddition,
                            handleAccordionState,
                            handleAccordionClick,
                            changeOrderingUp,
                            changeOrderingDown,
                            openedAccordion,
                            isEditable,
                            editHeading,
                            saveTitle,
                            entityName
                        }) => {
    let elem = null;
    return (
        <div>
            {/*{!!loader &&*/}
            {/*<Loader/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-courses1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >{entityName}
                </h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-edit__cursor" : ""}/>

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
                        // onChange={(value) => handleAccordionClick(value, fields, error)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                    >
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).name_of_certification || 'Course'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteCourse(index, fields, event)}
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
                                                            <label>Course Name</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-courses-gr"/>
                                                                </div>
                                                                <Field component={renderField}
                                                                       type={"text"}
                                                                       name={`${member}.name_of_certification`}
                                                                       className={"input-control"}/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Completion Year</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker}
                                                                       type={"date"}
                                                                       name={`${member}.year_of_certification`}
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

class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteCourse = this.deleteCourse.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
        }
    }

    componentDidMount() {
        this.props.fetchUserCourse()
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }

    }


    handleAddition(fields, error) {
        const listLength = fields.length;

        // if (listLength) this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "name_of_certification": '',
            "year_of_certification": '',
            order: fields.length
        })
    }

    deleteCourse(index, fields, event) {
        event.stopPropagation();
        const course = fields.get(index);
        fields.remove(index);
        if (course && course.id) {
            this.props.removeCourse(course.id)
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
            handleSubmit, ui: {loader}, editHeading, saveTitle, isEditable,
            entityName, nextEntity, handlePreview, changeOrderingUp, changeOrderingDown
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={'list'}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAccordionState={this.handleAccordionState}
                            handleAddition={this.handleAddition}
                            deleteCourse={this.deleteCourse}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            openedAccordion={this.state.openedAccordion}
                            component={CourseRenderer}
                            saveTitle={(event) => saveTitle(event, 7)}
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


export const
    CourseForm = reduxForm({
        form: 'course',
        enableReinitialize: true,
        validate
    })(Course);


const
    mapStateToProps = (state) => {
        return {
            initialValues: state.course,
            ui: state.ui
        }
    };

const
    mapDispatchToProps = (dispatch) => {
        return {
            "onSubmit": (userCourse) => {
                const {year_of_certification} = userCourse;
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                    }
                };
                return new Promise((resolve, reject) => {
                    return dispatch(actions.updateUserCourse({userCourse, resolve, reject}));
                })
            },
            "fetchUserCourse": () => {
                return dispatch(actions.fetchUserCourse())
            },
            "removeCourse": (courseId) => {
                return dispatch(actions.deleteCourse(courseId))
            },

            "bulkUpdateOrCreate": (listItems) => {
                listItems = (listItems || []).map(userCourse => {
                    const {year_of_certification} = userCourse;
                    if (!userCourse['id']) delete userCourse['id'];
                    userCourse = {
                        ...userCourse,
                        ...{
                            year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                        }
                    };
                    return userCourse;
                });
                return new Promise((resolve, reject) => {
                    return dispatch(actions.bulkUpdateOrCreateUserCourse({list: listItems, resolve, reject}))
                })

            },
            "handleSwap":
                (listItems) => {
                    listItems = (listItems || []).map(userCourse => {
                        const {year_of_certification} = userCourse;
                        if (!userCourse['id']) delete userCourse['id'];
                        userCourse = {
                            ...userCourse,
                            ...{
                                year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                            }
                        };
                        return userCourse;
                    })
                    return dispatch(actions.handleCourseSwap({list: listItems}))
                }
        }
    };

export default connect(mapStateToProps, mapDispatchToProps)

(
    CourseForm
)
;
