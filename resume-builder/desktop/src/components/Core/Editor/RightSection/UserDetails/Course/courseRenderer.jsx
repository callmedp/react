import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import { Field } from "redux-form";
import styles from './course.scss'
import { yearList } from '../../../../../../Utils/yearList'
import { renderField, renderSelect } from "../../../../../FormHandler/formFieldRenderer";
import React from "react";

export const CourseRenderer = ({
    fields,
    loader,
    meta: { touched, error, submitFailed },
    handleSubmit,
    deleteCourse,
    handleAddition,
    handleAccordionClick,
    changeOrderingUp,
    changeOrderingDown,
    isEditable,
    editHeading,
    saveTitle,
    entityName,
    expanded,
    handleInputValue,
    showAlertMessage
}) => {
    return (
        <div>
            {/*{!!loader &&*/}
            {/*<Loader/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-courses1" /></span>
                {!!(!isEditable) ?
                    <h2>{entityName}
                    </h2> :
                    <React.Fragment>
                        <input autoFocus type="text" name="" defaultValue={entityName}
                            onChange={(event) => handleInputValue(event.target.value || entityName)} maxLength="20" />
                        <span onClick={(event) => saveTitle(event)} className="icon-tick" />
                    </React.Fragment>
                }
                <span onClick={() => editHeading()}
                    className={!!(!isEditable) ? "icon-edit " + styles['icon-edit__cursor'] : ""} />

                <button
                    onClick={handleSubmit((values) => {
                        let skipAddition = false;
                        (values && values.list  || []).forEach(el => {
                            if (!el.name_of_certification) {
                                skipAddition = true;
                            }
                        })
                        if (!skipAddition) {
                            handleAddition(fields, error)
                        }
                        else {
                            showAlertMessage()
                        }
                    })}

                    type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>


            </section>
            <section className="right-sidebar-scroll" id="course">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                    >
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index} id={`course${index}`}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className={"add-section-heading"}>{fields.get(index).name_of_certification || 'Course'}</h3>
                                                            <span
                                                                className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteCourse(index, fields, event)}
                                                                    className="icon-delete mr-15" />
                                                                {index !== 0 &&
                                                                    <span
                                                                        onClick={(event) => changeOrderingUp(index, fields, event)}
                                                                        className="icon-ascend mr-5" />
                                                                }
                                                                {
                                                                    index !== fields.length - 1 &&
                                                                    < span
                                                                        onClick={(event) => changeOrderingDown(index, fields, event)}
                                                                        className="icon-descend" />
                                                                }
                                                            </div>
                                                        </div>
                                                    </AccordionItemButton>
                                                </AccordionItemHeading>
                                                <AccordionItemPanel>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Course Name</label>
                                                            <Field
                                                                autoFocus={true}
                                                                iconClass={'icon-courses-gr'}
                                                                component={renderField}
                                                                maxLength={'50'}
                                                                type={"text"}
                                                                name={`${member}.name_of_certification`}
                                                                className={"input-control"} />
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Completion Year</label>
                                                            <Field
                                                                iconClass={'icon-date'}
                                                                component={renderSelect}
                                                                options={yearList}
                                                                isMulti={false}
                                                                name={`${member}.year_of_certification`}
                                                                className="input-control" />


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