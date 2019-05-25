import React from 'react';
import {Field} from "redux-form";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";
import DataLoader from "../../../../../Common/DataLoader/dataloader"
import {courseNewData} from "../../../../../../Utils/addnewData"

const renderCourse = ({
                        fields, 
                        meta: {touched, error, submitFailed},
                        handleSubmit,
                        handleAddition,
                        deleteCourse,
                        changeOrderingUp,
                        changeOrderingDown,
                        editHeading,
                        heading,
                        updateInputValue,
                        loader,
                        editHeadingClick}) => 
{
    return (
        
        <div className="buildResume__wrap">
                {loader ? <DataLoader/> : ""}
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    {!editHeading ?
                        <React.Fragment>
                            <h1>{heading}</h1>
                            <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus placeholder={heading} onBlur={(e)=>updateInputValue('blur',e)}
                                onKeyDown={(e)=>updateInputValue('keyPress',e)}/>
                            <i className="sprite icon--editTick"></i>
                        </React.Fragment>
                    }   
                </div>
                {!editHeading ?
                    <button role="button" className="btn btn__round btn--outline"
                        onClick={handleSubmit(handleAddition.bind(this,fields,courseNewData(fields),0,'course'))}
                        type={'button'}>+ Add new</button>:''
                }
            </div>
            {fields.map((member, index) => {
            return (
                <div className="form-wrap" key={index} id={`course${index}`}>
                    <div className="subHeading pb-0">
                        <h2>{fields.get(index).name_of_certification || 'Course'}</h2>
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className={"sprite icon--delete " +(fields.length === 1 && !fields.get(index).id ? "hide":"")}
                                onClick={(event) => deleteCourse(index, fields, event)}
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
                            <Field component={renderField} label={"Course name"}  type={"text"} name={`${member}.name_of_certification`} prepend={true}
                                id={`${member}.name_of_certification`} iconClass={"sprite icon--course-grey"} className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={datepicker} label={"Completion Year"}  type={"date"} 
                                name={`${member}.year_of_certification`} id={`${member}.year_of_certification`}/>
                        </li>

                    </ul>
                </div>
            )})}
        </div>

    )
}

export default renderCourse