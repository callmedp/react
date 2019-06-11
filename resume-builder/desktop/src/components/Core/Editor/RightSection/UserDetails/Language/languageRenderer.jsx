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
import styles from './language.scss'

export const LanguageRenderer = ({
                                     fields,
                                     loader,
                                     meta: {touched, error, submitFailed},
                                     deleteLanguage,
                                     handleSubmit,
                                     handleAddition,
                                     handleAccordionClick,
                                     changeOrderingUp,
                                     changeOrderingDown,
                                     entity,
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
                <span className="icon-box"><i className="icon-languages1"/></span>
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
                      className={!!(!isEditable) ? "icon-edit " + styles['icon-language__cursor'] : ""}/>

                <button onClick={handleSubmit((values) => {
                    handleAddition(fields, error)
                })}
                        type={'button'}
                        className={"add-button " + styles['add-button__right']}>Add new
                </button>

            </section>
            <section className="right-sidebar-scroll" id="language">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value)}
                        allowZeroExpanded={false}
                        allowMultipleExpanded={true}
                        preExpanded={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}>
                        {fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index} id={`language${index}`}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className={"add-section-heading"}>{fields.get(index).name || 'Language'}</h3>
                                                            <span
                                                                className={expanded.indexOf(index) > -1 ? "opened-accordion" : "closed-accordion"}></span>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteLanguage(index, fields, event)}
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
                                                        <fieldset className="width-half">
                                                            <label>Language name</label>
                                                            <Field
                                                                autoFocus={true}
                                                                iconClass={'icon-language-gr'}
                                                                component={renderField} type={"text"}
                                                                name={`${member}.name`}
                                                                className={"input-control"}/>
                                                        </fieldset>

                                                        <fieldset className={styles['width-half']}>
                                                            <label>Language rating (out of 10)</label>
                                                            <Field
                                                                iconClass={'icon-rating'}
                                                                name={`${member}.proficiency`}
                                                                component={renderSelect}
                                                                closeMenuOnSelect={true}
                                                                isMulti={false}
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
                                                                ]}/>
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
                            }
                        )}
                    </Accordion>
                </ul>
            </section>


        </div>
    )
}
