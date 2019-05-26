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
                                      expanded,
                                      handleInputValue
                                  }) => {

    return (
        <div>
            {/*{!!loader &&*/}
            {/*<LoaderSection/>*/}
            {/*}*/}
            <section className="head-section">
                <span className="icon-box"><i className="icon-references1"/></span>
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
                <section className="right-sidebar-scroll" id="reference">
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
                                                <AccordionItem uuid={index} id={`reference${index}`}>
                                                    <AccordionItemHeading>
                                                        <AccordionItemButton>
                                                            <div className="flex-container">
                                                                <h3 className={"add-section-heading"}>{fields.get(index).reference_name || 'Reference'}</h3>
                                                                <span
                                                                    className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
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

                                                                <Field
                                                                    autoFocus={true}
                                                                    iconClass={'icon-refrences-gr'}
                                                                    component={renderField} type={"text"}
                                                                    name={`${member}.reference_name`}
                                                                    className={"input-control"}
                                                                />
                                                            </fieldset>
                                                            <fieldset>
                                                                <label>Designation</label>
                                                                <Field
                                                                    iconClass={'icon-designation'}
                                                                    component={renderField} type={"text"}
                                                                    name={`${member}.reference_designation`}
                                                                    className={"input-control"}
                                                                />
                                                            </fieldset>
                                                        </div>

                                                        <div className="flex-container">
                                                            <fieldset>
                                                                <label>Description</label>
                                                                <Field component={renderTextArea}
                                                                       noIcon={true}
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
