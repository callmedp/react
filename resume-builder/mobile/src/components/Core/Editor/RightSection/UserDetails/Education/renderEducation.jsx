import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import React from 'react';
import {Field} from "redux-form";
import DataLoader from "../../../../../Common/DataLoader/dataloader"

const renderEducation = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            handleAddition,
                            deleteEducation,
                            changeOrderingDown,
                            changeOrderingUp,
                            editHeading,
                            heading,
                            updateInputValue,
                            editHeadingClick
                        }) => {
    return (
        
        <div className="buildResume__wrap">
                {/* <DataLoader/> */}
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    {!editHeading ?
                            <h1>{heading}</h1>:
                            <input type="text" autoFocus placeholder={heading} onBlur={(e)=>updateInputValue('blur',e)}
                            onKeyDown={(e)=>updateInputValue('keyPress',e)}/>
                        }
                        <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                </div>
                
                <button role="button" className="btn btn__round btn--outline"
                    onClick={handleSubmit(handleAddition.bind(this,fields, error))}
                    type={'button'}>+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return(
                    <div className="form-wrap" key={index} id={`education${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).institution_name || 'Education'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className={"sprite icon--delete " +(fields.get(index).id ? "":"hide")} 
                                    onClick={(event) => deleteEducation(index, fields, event)}
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
                                <Field component={renderField} label={"Institution Name"}  type={"text"} name={`${member}.institution_name`} prepend={true} 
                                    id={`${member}.institution_name`} iconClass={"sprite icon--education-grey"} className="form__input"/>
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Specialization"}  type={"text"} name={`${member}.specialization`} prepend={true} 
                                    id={`${member}.specialization`} iconClass={"sprite icon--date"} className="form__input"/>
                            </li>
                            
                            <li className="form__group">
                                <Field component={datepicker} label={"Date from"}  type={"date"} 
                                    name={`${member}.start_date`} id={`${member}.start_date`}/>
                            </li>

                            <li className="form__group">
                                <Field component={datepicker} label={"Date to"}  type={"date"} 
                                    name={`${member}.end_date`} id={`${member}.end_date`}/>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <Field type="checkbox" name={`${member}.is_pursuing`} component="input" 
                                    className="form__radio-input" id={`${member}.is_pursuing`}/>
                                <label className="form__radio-label" htmlFor={`${member}.is_pursuing`}>
                                    <span className="form__radio-button"></span>
                                    Till today
                                </label>
                            </li>

                            <li className="form__group">
                                <Field component={renderSelect} label={"Course Type"} name={`${member}.course_type`} prepend={true} 
                                    id={`${member}.course_type`} iconClass={"sprite icon--date"} className="form__input">
                                    <option value="">Choose</option>
                                    <option value="FT" >FULL TIME</option>
                                    <option value="PT" >PART TIME</option>
                                </Field>
                            </li>
                            
                            <li className="form__group">
                                <Field component={renderField} label={"Percentage/CGPA"}  type={"text"} name={`${member}.percentage_cgpa`} 
                                    id={`${member}.percentage_cgpa`} iconClass={"sprite icon--date"} className="form__input" prepend={true}/>
                            </li>

                        </ul>
                    </div>
                )
                
            })}

                
        </div>
    
    )
}

export default renderEducation;