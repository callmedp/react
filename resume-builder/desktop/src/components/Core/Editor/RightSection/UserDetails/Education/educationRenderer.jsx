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
import styles from './education.scss'

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
                                      expanded,
                                      till_today,
                                      tillTodayDisable,
                                      handleInputValue
                                  }) => {
    return (
        <div>
            {/*{<LoaderSection/>}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-education1"></i></span>
               {!!(!isEditable) ?
                    <h2>{entityName}
                    </h2> :
                    <React.Fragment>
                        <input autoFocus type="text" name="" defaultValue={entityName}
                               onChange={(event) => handleInputValue(event.target.value || entityName)}/>
                        <span onClick={(event) => saveTitle(event)} className="icon-tick"/>
                    </React.Fragment>
                }
                <span onClick={() => editHeading()}
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-education__cursor'] : ''}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>


            </section>


            <section className="right-sidebar-scroll" id="education">
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
                                            <AccordionItem uuid={index} name={`education${index}`}
                                                           id={`education${index}`}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className={"add-section-heading"}>{fields.get(index).specialization || 'Education'}</h3>
                                                            <span
                                                                className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
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
                                                            <Field
                                                                autoFocus={true}
                                                                iconClass={'icon-company'}
                                                                maxLength={'50'}
                                                                component={renderField} type={"text"}
                                                                name={`${member}.institution_name`}/>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Specialization</label>
                                                            <Field
                                                                iconClass={'icon-designation'}
                                                                component={renderField}
                                                                maxLength={'50'}
                                                                type={"text"}
                                                                name={`${member}.specialization`}/>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Date from</label>
                                                            <Field maxDateAllowed={true} component={datepicker}
                                                                   type={"date"}
                                                                   iconClass={'icon-date'}
                                                                   yearDropDownItemNumber={15}
                                                                   name={`${member}.start_date`}
                                                                   className="input-control"/>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date to</label>
                                                            <Field component={datepicker}
                                                                   type={"date"}
                                                                   iconClass={'icon-date'}
                                                                   name={`${member}.end_date`}
                                                                   disabled={till_today[index]}
                                                                   yearDropDownItemNumber={15}
                                                                   className="input-control"/>

                                                            <span className={styles["till-today"]}>
                                                                <Field type="checkbox" name={`${member}.is_pursuing`}
                                                                       component={renderField}
                                                                       tillTodayDisable={tillTodayDisable}
                                                                       index={`${index}`}
                                                                       text={'Till Today'}
                                                                       checked={`${member}.end_date` === true}/>
                                                            </span>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">

                                                        <fieldset className="custom">
                                                            <label>Course Type</label>
                                                            <Field
                                                                iconClass={'icon-course-type'}
                                                                component={renderSelect} type={"text"}
                                                                name={`${member}.course_type`}
                                                                options={[
                                                                    {value: 'FT', label: 'FULL TIME'},
                                                                    {value: 'PT', label: 'PART TIME'},
                                                                ]}
                                                                closeMenuOnSelect={true}
                                                                className="input-control"/>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Percentage</label>
                                                            <Field
                                                                iconClass={'icon-percentage'}
                                                                component={renderField} type={"text"}
                                                                name={`${member}.percentage_cgpa`}
                                                                className="input-control"/>

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
