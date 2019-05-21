import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import styles from './award.scss'
import {Field} from "redux-form";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";

export const AwardRenderer = ({
                                  fields,
                                  loader,
                                  meta: {touched, error, submitFailed},
                                  handleSubmit,
                                  deleteAward,
                                  handleAddition,
                                  handleAccordionClick,
                                  changeOrderingUp,
                                  changeOrderingDown,
                                  openedAccordion,
                                  isEditable,
                                  editHeading,
                                  saveTitle,
                                  entityName,
                                  expanded
                              }) => {
    let elem = null;
    return (
        <div>
            {/*{!!(loader) &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className={'head-section'}>
                <span className={'icon-box'}><i className={'icon-awards1'}/></span>
                <h2 className={"comp-heading"} ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? 'icon-edit ' + styles['icon-awards__cursor'] : ""}/>

                <button onClick={handleSubmit((values) => {
                    handleAddition(fields, error)
                })}
                        type={'button'}
                        className={'add-button ' + styles['add-button__right']}>Add new
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
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                             <h3 className={"add-section-heading"}>{fields.get(index).title || 'Award'}</h3>
                                                            <span className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteAward(index, fields, event)}
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
                                                            <label>Title</label>
                                                            <Field
                                                                iconClass={'icon-awards-gr'}
                                                                component={renderField} type={"text"}
                                                                name={`${member}.title`}
                                                                className="input-control"/>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date</label>
                                                            <Field
                                                                iconClass={'icon-date'}
                                                                component={datepicker}
                                                                maxDateAllowed={true}
                                                                yearDropDownItemNumber={30}
                                                                type={"date"}
                                                                className={'input-control'}
                                                                name={`${member}.date`}/>
                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Summary</label>
                                                            <Field
                                                                noIcon={true}
                                                                component={renderTextArea} type={"textarea"}
                                                                name={`${member}.summary`}
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
