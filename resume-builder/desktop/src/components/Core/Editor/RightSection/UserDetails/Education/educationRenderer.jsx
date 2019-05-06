import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import {Field} from "redux-form";
import {datepicker, renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";

export const EducationRenderer = ({
                                      fields,
                                      loader,
                                      meta: {touched, error, submitFailed},
                                      deleteEducation,
                                      handleAddition,
                                      handleSubmit,
                                      handleAccordionClick,
                                      changeOrderingUp,
                                      changeOrderingDown,
                                      editHeading,
                                      saveTitle,
                                      isEditable,
                                      entityName,
                                      expanded
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
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
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
                                                            <h3 className={"add-section-heading" + (expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion")}>{fields.get(index).specialization || 'Education'}</h3>
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
                                    <Field type="checkbox" name={`${member}.is_pursuing`} component={renderField}  checked={`${member}.end_date` === true}/>
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
