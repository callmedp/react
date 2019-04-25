import React from 'react';
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {Field} from "redux-form";

export const renderAwards = ({
                                fields, 
                                meta: {touched, error, submitFailed},
                                handleSubmit,
                                handleAddition,
                                deleteAward,
                                changeOrderingUp,
                                changeOrderingDown,
                            }) => {
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>Award</h1>
                    <input className="hide" type="text" placeholder="Award"/>
                    <i className="sprite icon--edit"></i>
                </div>
                <button role="button" onClick={handleSubmit(handleAddition.bind(this, fields, error))}
                    type={'button'} className="btn btn__round btn--outline">+ Add new</button>
            </div>

            {fields.map((member, index) => {
            return(
                <div className="form-wrap" key={index} id={`award${index}`}>
                    <div className="subHeading pb-0">
                        <h2>{fields.get(index).title || 'Award'}</h2>

                        
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className="sprite icon--delete" role="button"
                                    onClick={(event) => deleteAward(index, fields, event)}></span>
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
                                        <i className="sprite icon--date"></i>
                                    </span>
                                </div>
                                <Field component={renderTextArea} type={"textarea"} className={'form__input'}
                                    className="form__input" name={`${member}.summary`}/>
                            </div>
                        </li>
                    </ul>
                </div>
            )})}
            {error && <li>{error}</li>}
        </div>
            
    )
}

export default renderAwards