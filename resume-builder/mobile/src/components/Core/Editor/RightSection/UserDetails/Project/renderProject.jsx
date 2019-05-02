import React from 'react';
import {Field} from "redux-form";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import DataLoader from "../../../../../Common/DataLoader/dataloader"

const renderProjects = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            handleAddition,
                            deleteProject,
                            changeOrderingUp,
                            changeOrderingDown,
                            editHeading,
                            heading,
                            updateInputValue,
                            editHeadingClick,
                            loader
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
                <button role="button" className="btn btn__round btn--outline"
                    onClick={handleSubmit(handleAddition.bind(this,fields, error))}
                    type={'button'}>+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return (
                    <div className="form-wrap" key={index} id={`project${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).project_name || 'Project'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className={"sprite icon--delete " +(fields.length === 1 && !fields.get(index).id ? "hide":"")} 
                                    onClick={(event) => deleteProject(index, fields, event)}
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
                                <Field component={renderField} label={"Project name"}  type={"text"} name={`${member}.project_name`} prepend={true} 
                                    id={`${member}.project_name`} iconClass={"sprite icon--project-gray"} className="form__input"/>
                            </li>
    
                            <li className="form__group">
                                <Field component={datepicker} label={"Date from"}  type={"date"} 
                                    name={`${member}.start_date`} id={`${member}.start_date`}/>
                            </li>

                            <li className="form__group">
                                <Field component={datepicker} label={"Date to"}  type={"date"} 
                                    name={`${member}.end_date`} id={`${member}.end_date`}/>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="description">Description</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderTextArea} rows={"3"} type={"textarea"}
                                        className="form__input" name={`${member}.description`}
                                        value={`${member}.description`}/>
                                </div>
                            </li>
                        </ul>
                    </div>
                )})}      
        </div>
    
    )
}

export default renderProjects