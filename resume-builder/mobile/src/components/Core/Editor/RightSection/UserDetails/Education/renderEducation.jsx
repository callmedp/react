import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import React from 'react';
import {Field} from "redux-form";

const renderEducation = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleAddition,
                            deleteEducation,
                            changeOrderingDown,
                            changeOrderingUp
                        }) => {
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>Education</h1>
                    <i className="sprite icon--edit"></i>
                </div>
                <button role="button" className="btn btn__round btn--outline"
                    onClick={(event) => handleAddition(fields, error, event)}
                    type={'button'}>+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return(
                    <div className="form-wrap" key={index}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).institution_name || 'Education'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" 
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
                                <label className="form__label" htmlFor="institution_name">Institution Name </label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--education-grey"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} name={`${member}.institution_name`}
                                    className="form__input"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="specialization">Specialization</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"}
                                    name={`${member}.specialization`} className="form__input"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="start_date">Date from</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={datepicker} type={"date"} 
                                    name={`${member}.start_date`}/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="end_date">Date to</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={datepicker} type={"date"} 
                                    name={`${member}.end_date`}/>
                                </div>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <Field type="radio" name={`${member}.is_pursuing`} component="input" 
                                    className="form__radio-input" value={`${member}.is_pursuing`}/>
                                <label className="form__radio-label" htmlFor="tillToday">
                                    <span className="form__radio-button"></span>
                                    Till today
                            </label>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="course_type">Course Type</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field name={`${member}.course_type`}
                                            component={renderSelect} className="form__input">
                                        <option value="">Choose</option>
                                        <option value="FT" >FULL TIME</option>
                                        <option value="PT" >PART TIME</option>
                                    </Field>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="percentage_cgpa">Percentage/CGPA</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderField} type={"text"} 
                                    name={`${member}.percentage_cgpa`} className="form__input"/>
                                </div>
                            </li>

                        </ul>
                    </div>
                )
                
            })}

                
        </div>
    
    )
}

export default renderEducation;