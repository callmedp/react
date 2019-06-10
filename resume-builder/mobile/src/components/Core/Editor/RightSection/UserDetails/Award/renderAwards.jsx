import React from 'react';
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {Field} from "redux-form";
import {awardNewData} from "../../../../../../Utils/addnewData"

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
                            }) => {
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    {!editHeading ?
                        <React.Fragment>
                            <h1>{heading}</h1>
                            <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} onBlur={(e)=>updateInputValue('blur',e)}
                                onKeyDown={(e)=>updateInputValue('keyPress',e)} maxLength="20"/>
                            <i className="sprite icon--editTick"></i>
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
                                id={`${member}.title`} iconClass={"sprite icon--education-grey"} className="form__input"/>
                        </li>

                        <li className="form__group">
                            <Field component={datepicker} label={"Date"}  type={"date"} 
                                name={`${member}.date`} id={`${member}.date`}/>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="summary">Summary</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--course-type"></i>
                                    </span>
                                </div>
                                <Field component={renderTextArea} type={"textarea"} className={'form__input'}
                                    className="form__input" name={`${member}.summary`}/>
                            </div>
                        </li>
                    </ul>
                </div>
            )})}
        </div>
            
    )
}

export default renderAwards