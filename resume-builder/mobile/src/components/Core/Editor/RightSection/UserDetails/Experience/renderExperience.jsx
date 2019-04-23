import React from 'react';
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field} from 'redux-form';


const renderExperiences = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleAddition,
                            deleteExperience,
                            changeOrderingUp,
                            changeOrderingDown,
                            }) => {
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>Experience</h1>
                    <i className="sprite icon--edit"></i>
                </div>
                <button role="button"
                onClick={handleAddition.bind(this, fields, error)}
                type={'button'} className="btn btn__round btn--outline">+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return (
                <div className="form-wrap" key={index}>
                    <div className="subHeading pb-0">
                        <h2>{fields.get(index).company_name || 'Experience'}</h2>
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className="sprite icon--delete"
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
                            <label className="form__label" htmlFor="job_profile">Designation</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--designation"></i>
                                    </span>
                                </div>
                                <Field component={renderField} type={"text"} 
                                name={`${member}.job_profile`} className="form__input"  />
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="company_name">Company name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--company"></i>
                                    </span>
                                </div>
                                <Field component={renderField} type={"text"} 
                                name={`${member}.company_name`} className="form__input"/>
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
                            <Field type="checkbox" name={`${member}.is_working`}component="input" 
                                className="form__radio-input" id={`${member}.is_working`} value={`${member}.is_working`}/>
                            <label className="form__radio-label" htmlFor={`${member}.is_working`}>
                                <span className="form__radio-button"></span>
                                Till today
                            </label>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="job_location">Job Location</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--company"></i>
                                    </span>
                                </div>
                                <Field component={renderField} type={"text"} 
                                name={`${member}.job_location`} className="form__input"/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="work_description">Description</label>
                            <Field component={renderTextArea} type={"textarea"} name={`${member}.work_description`}
                                className="form__input h-300" rows="5" 
                            />
                        </li>

                    </ul>
                </div>
                )
            })}
            
        </div>

    )
}

export default renderExperiences