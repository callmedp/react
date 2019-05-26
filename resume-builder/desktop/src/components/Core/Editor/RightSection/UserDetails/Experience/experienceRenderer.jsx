import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import {Field} from "redux-form";
import {
    datepicker,
    renderField,
    renderTextArea,
    renderDynamicSelect
} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";
import styles from './experience.scss'


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
                                       expanded,
                                       fetchJobTitles,
                                       till_today,
                                       tillTodayDisable,
                                       handleInputValue,
                                       showSuggestionModal

                                   }) => {
    return (
        <div>
            <section className="head-section">
                <span className="icon-box"><i className="icon-experience1"/></span>
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
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-experience__cursor'] : ''}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>

            </section>


            <section className="right-sidebar-scroll" id="experience">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}>
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index} name={`experience${index}`} id={`experience${index}`}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className={"add-section-heading"}>{fields.get(index).job_profile.value || 'Experience'}</h3>
                                                            <span
                                                                className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
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
                                                        <fieldset>
                                                            <label>Designation</label>
                                                            <Field
                                                                // autoFocus={true}
                                                                iconClass={'icon-designation'}
                                                                component={renderDynamicSelect}
                                                                closeMenuOnSelect={false}
                                                                isMulti={false}
                                                                loadOptions={(inputValue) => fetchJobTitles(inputValue)}
                                                                defaultOptions={[{value: 'aman', label: "aman"}]}
                                                                name={`${member}.job_profile`}/>

                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Company Name</label>
                                                            <Field
                                                                iconClass={'icon-company'}
                                                                component={renderField}
                                                                type={"text"}
                                                                name={`${member}.company_name`}/>

                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Date from</label>

                                                            <Field component={datepicker}
                                                                   type={"date"}
                                                                   yearDropDownItemNumber={15}
                                                                   maxDateAllowed={true}
                                                                   iconClass={'icon-date'}
                                                                   className={'input-control'}
                                                                   name={`${member}.start_date`}/>

                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date to</label>
                                                            <Field component={datepicker}
                                                                   disabled={till_today[index]}
                                                                   type={"date"}
                                                                   iconClass={'icon-date'}
                                                                   name={`${member}.end_date`}
                                                                   className={'input-control'}/>

                                                            <span className={styles['till-today']}>
                                                                <Field type="checkbox"
                                                                       name={`${member}.is_working`}
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
                                                            <label>Job Location</label>
                                                            <Field
                                                                iconClass={'icon-address'}
                                                                component={renderField} type={"text"}
                                                                name={`${member}.job_location`}
                                                                className={"input-control"}/>

                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Description</label>
                                                            <Field component={renderTextArea} rows={"3"}
                                                                   type={"text"}
                                                                   noIcon={true}
                                                                   name={`${member}.work_description`}/>
                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <span className="add-suggested"
                                                                  onClick={showSuggestionModal}>Add suggested experience</span>

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