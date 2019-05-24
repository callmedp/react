import React from 'react';
import {renderField, renderTextArea, datepicker,renderCheckboxField} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field} from 'redux-form';
import DataLoader from "../../../../../Common/DataLoader/dataloader"
import {experienceNewData} from "../../../../../../Utils/addnewData"


const renderExperiences = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            handleAddition,
                            deleteExperience,
                            changeOrderingUp,
                            changeOrderingDown,
                            editHeading,
                            heading,
                            updateInputValue,
                            editHeadingClick,
                            loader,
                            till_today,
                            tillTodayDisable
                            }) => {
    return (
        
        <div className="buildResume__wrap">
                {loader ? <DataLoader/> :""}
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    {!editHeading ?
                        <h1>{heading}</h1>:
                        <input type="text" autoFocus placeholder={heading} onBlur={(e)=>updateInputValue('blur',e)}
                         onKeyDown={(e)=>updateInputValue('keyPress',e)}/>
                    }
                    <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                </div>
                {!editHeading ?
                    <button role="button"
                        onClick={handleSubmit(handleAddition.bind(this,fields,experienceNewData(fields),780,'experience'))}
                        type={'button'} className="btn btn__round btn--outline">+ Add new</button>:''
                }
            </div>
            {fields.map((member, index) => {
                return (
                <div className="form-wrap" key={index} id={`experience${index}`} >
                    <div className="subHeading pb-0">
                        <h2>{fields.get(index).company_name || 'Experience'}</h2>
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className={"sprite icon--delete " +(fields.length === 1 && !fields.get(index).id ? "hide":"")}
                                onClick={(event) => deleteExperience(index, fields, event)}
                                role="button"></span>
                            </li>
                            {index == 0 ? '':
                                <li className="subHeading__btn"
                                    onClick={(event) => changeOrderingUp(index, fields, event)}>
                                    <i className="sprite icon--upArrow"></i>
                                </li>
                            }
                            {index == fields.length-1 ? '':
                                <li className="subHeading__btn"
                                    onClick={(event) => changeOrderingDown(index, fields, event)}>
                                    <i className="sprite icon--downArrow"></i>
                                </li>
                            }
                        </ul>
                    </div>

                    <ul className="form pb-0">

                        <li className="form__group">
                            <Field component={renderField} label={"Designation"}  type={"text"} name={`${member}.job_profile`} prepend={true} 
                                id={`${member}.job_profile`} iconClass={"sprite icon--designation"} className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={renderField} label={"Company name"}  type={"text"} name={`${member}.company_name`} 
                                id={`${member}.company_name`} iconClass={"sprite icon--company"} className="form__input" prepend={true}/>
                        </li>

                        <li className="form__group">
                            <Field component={datepicker} label={"Date from"}  type={"date"} yearDropDownItemNumber={15}
                                name={`${member}.start_date`} id={`${member}.start_date`}/>
                        </li>

                        <li className="form__group">
                            <Field component={datepicker} label={"Date to"}  type={"date"} minDate={fields.get(index).start_date}
                                yearDropDownItemNumber={15} name={`${member}.end_date`} id={`${member}.end_date`} disabled={till_today[index]}/>
                        </li>

                        <li className="form__radio-group d-flex justify-content-end fs-14">
                            <Field type="checkbox" name={`${member}.is_working`} component={renderCheckboxField} 
                                className="form__radio-input" id={`${member}.is_working`} tillTodayDisable={tillTodayDisable}
                                index={`${index}`}  />
                            <label className="form__radio-label" htmlFor={`${member}.is_working`}>
                                <span className="form__radio-button"></span>
                                Till today
                            </label>
                            
                        </li>
                        
                        <li className="form__group">
                            <Field component={renderField} label={"Job Location"}  type={"text"} name={`${member}.job_location`} 
                                id={`${member}.job_location`} iconClass={"sprite icon--location"} className="form__input" prepend={true}/>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="work_description">Description</label>
                            <Field component={renderTextArea} type={"textarea"} name={`${member}.work_description`}
                                className="form__input h-150" rows="5" 
                            />
                        </li>

                    </ul>
                </div>
                )
            })}
            
        </div>

    )
}

export default renderExperiences;