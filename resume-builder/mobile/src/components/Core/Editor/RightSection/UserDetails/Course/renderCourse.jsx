import React from 'react';
import {Field} from "redux-form";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {courseNewData} from "../../../../../../Utils/addnewData"
import { yearList } from '../../../../../../Utils/yearList.js';

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
                        headingChange,
                        context,
                        entity_preference_data,
                        editHeadingClick}) => 
{
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    {!editHeading ?
                        <React.Fragment>
                            <h1 className="heading-style">{heading}</h1>
                            <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} maxLength={'20'}
                                    onChange={(event) => context.setState({heading:event.target.value})} />
                            <i className="sprite icon--editTick" 
                                onClick={()=>{headingChange(entity_preference_data,heading,7);context.setState({editHeading:false})}}></i>
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
                            {index === 0 ? '':
                                <li className="subHeading__btn"
                                    onClick={(event) =>{fields=changeOrderingUp(index, fields, event);context.setState({fields})}}>
                                    <i className="sprite icon--upArrow"></i>
                                </li>
                            }
                            {index === fields.length-1 ? '':
                                <li className="subHeading__btn"
                                    onClick={(event) =>{fields=changeOrderingDown(index, fields, event);context.setState({fields})}}>
                                    <i className="sprite icon--downArrow"></i>
                                </li>
                            }
                        </ul>
                    </div>

                    <ul className="form pb-0">
                            
                        <li className="form__group">
                            <Field component={renderField} label={"Course name"}  type={"text"} name={`${member}.name_of_certification`} prepend={true}
                                id={`${member}.name_of_certification`} iconClass={"sprite icon--course-grey"} className="form__input" maxLength={'50'}/>
                        </li>

                        <li className="form__group dob">
                            <Field component={renderSelect} label={"Year"} name={`${member}.year_of_certification`} prepend={true} 
                                    id={`${member}.year_of_certification`}  className="form__input" iconClass={"sprite icon--date"}>
                                    <option value="">Choose</option>
                                    {yearList.map((el)=>{
                                        return(
                                        <option value={el.value}>{el.label}</option>
                                        )
                                    })}
                                </Field>
                        </li>

                    </ul>
                </div>
            )})}
        </div>

    )
}

export default renderCourse