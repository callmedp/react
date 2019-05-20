import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import {Field} from "redux-form";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";
import styles from './skill.scss'


export const SkillRenderer = ({
                                  fields,
                                  loader,
                                  meta: {touched, error, submitFailed},
                                  deleteSkill,
                                  handleSubmit,
                                  handleAddition,
                                  handleAccordionClick,
                                  changeOrderingUp,
                                  changeOrderingDown,
                                  isEditable,
                                  editHeading,
                                  saveTitle,
                                  entityName,
                                  expanded
                              }) => {

    let elem = null;
    return (
        <div>
            {/*{!!loader &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-skills1"/></span>
                <h2
                    className={"comp-heading"}
                    ref={(value) => {
                        elem = value
                    }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-education__cursor'] : ""}
                />
                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>


            </section>

            <section className="right-sidebar-scroll" id="skill">
                <ul>
                    <Accordion

                        onChange={(value) => {
                            handleAccordionClick(value)
                        }}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}>
                        {fields.map((member, index) => {
                            return (
                                <li key={index}>
                                    <section className="info-section">
                                        <AccordionItem uuid={index} id={`skill${index}`}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="flex-container">
                                                         <h3 className={"add-section-heading"}>{fields.get(index).specialization || 'Skill'}</h3>
                                                            <span className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
                                                        <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteSkill(index, fields, event)}
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
                                                        <label>Skill name</label>
                                                        <div className="input-group">
                                                            <div className="input-group--input-group-icon">
                                                                <span className="icon-skills-gr"/>
                                                            </div>
                                                            <Field component={renderField}
                                                                   type={"text"} name={`${member}.name`}
                                                                   className={"input-control"}/>
                                                        </div>
                                                    </fieldset>

                                                    <fieldset className="custom">
                                                        <label>Skill rating (out of 10)</label>
                                                        <div className="input-group">
                                                            <div className="input-group--input-group-icon">
                                                                <span className="icon-rating"/>
                                                            </div>
                                                            <Field name={`${member}.proficiency`}
                                                                   component={renderSelect}
                                                                   isMulti={false}
                                                                   closeMenuOnSelect={true}
                                                                   options={[
                                                                       {value: 1, label: '1'},
                                                                       {value: 2, label: '2'},
                                                                       {value: 3, label: '3'},
                                                                       {value: 4, label: '4'},
                                                                       {value: 5, label: '5'},
                                                                       {value: 6, label: '6'},
                                                                       {value: 7, label: '7'},
                                                                       {value: 8, label: '8'},
                                                                       {value: 9, label: '9'},
                                                                       {value: 10, label: '10'}
                                                                   ]}
                                                            />
                                                        </div>
                                                    </fieldset>
                                                    <Field component={'input'} name={`${member}.id`}
                                                           type={'text'}
                                                           hidden={true}/>

                                                </div>

                                            </AccordionItemPanel>
                                        </AccordionItem>
                                    </section>
                                </li>
                            )
                        })}
                    </Accordion>
                </ul>
            </section>
        </div>

    );

}
