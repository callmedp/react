import React from 'react';
import {renderSelect, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {Field} from "redux-form";
import {awardNewData} from "../../../../../../Utils/addnewData"
import {yearList} from "../../../../../../Utils/yearList"

export const renderAwards = ({
                                fields, 
                                meta: {touched, error, submitFailed},
                                handleSubmit,
                                handleAddition,
                                deleteAward,
                                changeOrderingUp,
                                changeOrderingDown,
                                editHeading,
                                heading,
                                updateInputValue,
                                editHeadingClick,
                                context,
                                headingChange,
                                entity_preference_data,
                            }) => {
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
                                onClick={()=>{headingChange(entity_preference_data,heading,6);context.setState({editHeading:false})}}></i>
                        </React.Fragment>
                    }
                </div>
                {!editHeading ?
                    <button role="button" onClick={handleSubmit(handleAddition.bind(this,fields,awardNewData(fields),100,'award'))}
                        type={'button'} className="btn btn__round btn--outline">+ Add new</button>:''
                }
            </div>

            {fields.map((member, index) => {
            return(
                <div className="form-wrap" key={index} id={`award${index}`}>
                    <div className="subHeading pb-0">
                        <h2>{fields.get(index).title || 'Award'}</h2>
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className={"sprite icon--delete " +(fields.length === 1 && !fields.get(index).id ? "hide":"")}  role="button"
                                    onClick={(event) => deleteAward(index, fields, event)}></span>
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
                            <Field component={renderField} label={"Title"}  type={"text"} name={`${member}.title`} prepend={true}
                                id={`${member}.title`} iconClass={"sprite icon--education-grey"} maxLength={'50'} className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={renderSelect} label={"Year"} name={`${member}.date`} prepend={true} 
                                    id={`${member}.date`}  className="form__input" iconClass={"sprite icon--date"}>
                                    <option value="">Choose</option>
                                    {yearList.map((el,index)=>{
                                        return(
                                        <option key={index} value={el.value}>{el.label}</option>
                                        )
                                    })}
                                </Field>
                            {/* <Field component={datepicker} label={"Date"}  type={"date"} 
                                name={`${member}.date`} id={`${member}.date`}/> */}
                        </li>

                        <li className="form__group">
                            <Field component={renderTextArea} type={"textarea"} className={'form__input'} label={'Summary'}
                                name={`${member}.summary`} maxLength={'300'} prepend={true} iconClass={"sprite icon--course-type"}
                                id={`${member}.summary`}/>
                        </li>
                    </ul>
                </div>
            )})}
        </div>
            
    )
}

export default renderAwards