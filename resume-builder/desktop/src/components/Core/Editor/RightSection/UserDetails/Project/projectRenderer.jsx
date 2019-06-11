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
                                    formValues,
                                    handleInputValue
                                }) => {

    return (
        <div>
            {/*{!!loader &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-projects1"/></span>
                {!!(!isEditable) ?
                    <h2>{entityName}
                    </h2> :
                    <React.Fragment>
                        <input autoFocus type="text" name="" defaultValue={entityName}
                               onChange={(event) => handleInputValue(event.target.value || entityName)} maxLength="20"/>
                        <span onClick={(event) => saveTitle(event)} className="icon-tick"/>
                    </React.Fragment>
                }
                <span onClick={() => editHeading()}
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
                                                            <h3 className={"add-section-heading"}>{fields.get(index).project_name || 'Project'}</h3>
                                                            <span
                                                                className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
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
                                                            <Field component={renderField}
                                                                   autoFocus={true}
                                                                   iconClass={'icon-projects-gr'}
                                                                   type={"text"}
                                                                   name={`${member}.project_name`}
                                                                   className={"input-control"}/>

                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Date from</label>

                                                            <Field component={datepicker}
                                                                   type={"date"}
                                                                   iconClass={'icon-date'}
                                                                   yearDropDownItemNumber={15}
                                                                   maxDateAllowed={true}
                                                                   className={'input-control'}
                                                                   name={`${member}.start_date`}/>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date to</label>

                                                            <Field component={datepicker} type={"date"}
                                                                   className={'input-control'}
                                                                   disabled={till_today[index]}
                                                                   iconClass={'icon-date'}
                                                                   dateFromName={`${member}.start_date`}
                                                                   formValues={formValues}
                                                                   name={`${member}.end_date`}/>

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
                                                                   noIcon={true}
                                                                   maxLength={'300'}
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
