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

export const ExperienceRenderer = ({
                                       fields,
                                       loader,
                                       meta: {touched, error, submitFailed},
                                       deleteExperience,
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
                                       entityName,
                                       expanded
                                   }) => {
    let elem = null;

    return (
        <div>
            <section className="head-section">
                <span className="icon-box"><i className="icon-experience1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}>{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-experience__cursor" : ''}/>

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
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}>
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className={"add-section-heading" + (expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion")}>{fields.get(index).company_name || 'Experience'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteExperience(index, fields, event)}
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
                                                            <label>Designation</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-designation"/>
                                                                </div>
                                                                <Field component={renderField}
                                                                       type={"text"}
                                                                       name={`${member}.job_profile`}/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Company Name</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-company"/>
                                                                </div>
                                                                <Field component={renderField}
                                                                       type={"text"}
                                                                       name={`${member}.company_name`}/>
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
                                                                <Field component={datepicker}
                                                                       type={"date"}
                                                                       name={`${member}.end_date`}
                                                                       className={'input-control'}/>
                                                            </div>
                                                            <span className="till-today">
									                                    <Field type="checkbox"
                                                                               name={`${member}.is_working`}
                                                                               component={renderField}
                                                                               checked={`${member}.is_working` === true}/>
								                                	Till Today
							                                    	</span>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Job Location</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-address"/>
                                                                </div>
                                                                <Field component={renderField} type={"text"}
                                                                       name={`${member}.job_location`}
                                                                       className={"input-control"}/>
                                                            </div>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Description</label>
                                                            <Field component={renderTextArea} rows={"3"}
                                                                   type={"text"}
                                                                   name={`${member}.work_description`}/>
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