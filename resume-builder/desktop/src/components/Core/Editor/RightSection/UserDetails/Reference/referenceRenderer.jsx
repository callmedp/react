import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import {Field} from "redux-form";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer";
import React from "react";
import styles from './reference.scss'

export const ReferenceRenderer = ({
                                      fields,
                                      loader,
                                      meta: {touched, error, submitFailed},
                                      deleteReference,
                                      handleAddition,
                                      handleSubmit,
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
                <span className="icon-box"><i className="icon-references1"/></span>
                <h2 className={"comp-heading"}
                    ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-references__cursor'] : ""}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })} type={'button'}
                    className={"add-button " + styles['add-button__right']}>Add new
                </button>


                {/*{(touched || submitFailed) && error && <span>{error}</span>}*/}
            </section>
            <section>
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
                                                                <h3 className={"add-section-heading" + (expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion")}>{fields.get(index).reference_name || 'Reference'}</h3>
                                                                <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteReference(index, fields, event)}
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
                                                                <label>Reference name</label>
                                                                <div className="input-group">
                                                                    <div
                                                                        className="input-group--input-group-icon">
                                                                                <span
                                                                                    className="icon-refrences-gr"/>
                                                                    </div>
                                                                    <Field component={renderField} type={"text"}
                                                                           name={`${member}.reference_name`}
                                                                           className={"input-control"}
                                                                    />
                                                                </div>
                                                            </fieldset>
                                                            <fieldset>
                                                                <label>Designation</label>
                                                                <div className="input-group">
                                                                    <div
                                                                        className="input-group--input-group-icon">
                                                                                <span
                                                                                    className="icon-designation"/>
                                                                    </div>
                                                                    <Field component={renderField} type={"text"}
                                                                           name={`${member}.reference_designation`}
                                                                           className={"input-control"}
                                                                    />
                                                                </div>
                                                            </fieldset>
                                                        </div>

                                                        <div className="flex-container">
                                                            <fieldset>
                                                                <label>Description</label>
                                                                <Field component={renderTextArea}
                                                                       type={"textarea"}
                                                                       name={`${member}.about_candidate`}/>
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
            </section>

        </div>

    )

}
