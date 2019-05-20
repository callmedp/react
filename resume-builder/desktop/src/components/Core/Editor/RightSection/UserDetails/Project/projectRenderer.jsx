import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import {Field} from "redux-form";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";
import styles from './project.scss'

export const ProjectRenderer = ({
                                    fields,
                                    loader,
                                    meta: {touched, error, submitFailed},
                                    deleteProject,
                                    handleSubmit,
                                    handleAddition,
                                    handleAccordionClick,
                                    changeOrderingUp,
                                    changeOrderingDown,
                                    editHeading,
                                    saveTitle,
                                    isEditable,
                                    entityName,
                                    expanded,
                                    tillTodayDisable,
                                    till_today,
                                    formValues
                                }) => {
    let elem = null;

    return (
        <div>
            {/*{!!loader &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-projects1"/></span>
                <h2 className={"comp-heading"}
                    ref={(value) => {
                        elem = value
                    }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}>{entityName}
                </h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-edit__cursor'] : ""}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>

            </section>
            <section className="right-sidebar-scroll" id="project">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}>
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index} id={`project${index}`}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                             <h3 className={"add-section-heading"}>{fields.get(index).specialization || 'Project'}</h3>
                                                            <span className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
                                                            <div className="addon-buttons mr-10">
                                                                    <span
                                                                        onClick={(event) => deleteProject(index, fields, event)}
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
                                                            <label>Project Name</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-projects-gr"/>
                                                                </div>
                                                                <Field component={renderField} type={"text"}
                                                                       name={`${member}.project_name`}
                                                                       className={"input-control"}/>
                                                            </div>
                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Date from</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker}
                                                                       type={"date"}
                                                                       yearDropDownItemNumber={15}
                                                                       maxDateAllowed={true}
                                                                       className={'input-control'}
                                                                       name={`${member}.start_date`}/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date to</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker} type={"date"}
                                                                       className={'input-control'}
                                                                       disabled={till_today[index]}
                                                                       dateFromName={`${member}.start_date`}
                                                                       formValues={formValues}
                                                                       name={`${member}.end_date`}/>
                                                            </div>
                                                            <span className={styles['till-today']}>
                                                                <Field type="checkbox"
                                                                       name={`${member}.currently_working`}
                                                                       component={renderField}
                                                                       tillTodayDisable={tillTodayDisable}
                                                                       index={`${index}`}
                                                                       text={'Till Today'}
                                                                       checked={`${member}.is_working` === true}/>

							                                </span>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Description</label>
                                                            <Field component={renderTextArea} rows={"3"}
                                                                   type={"text"}
                                                                   name={`${member}.description`}
                                                                   value={`${member}.description`}/>
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
