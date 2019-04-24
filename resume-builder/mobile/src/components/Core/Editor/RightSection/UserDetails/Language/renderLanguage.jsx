import React from 'react';
import {Field} from "redux-form";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";

const renderLanguage = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleAddition,
                            deleteLanguage,
                            changeOrderingUp,
                            changeOrderingDown,
                        }) => {
    return (
        
        <div className="buildResume__wrap pb-0">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>Language</h1>
                    <i className="sprite icon--edit"></i>
                </div>
                <button role="button" className="btn btn__round btn--outline"
                onClick={handleAddition.bind(this, fields, error)}
                type={'button'} >+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return (
                    <div key={index}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).name || 'Language'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" 
                                     onClick={(event) => deleteLanguage(index, fields, event)}
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
                                <Field component={renderField} label={"Language name"}  type={"text"} name={`${member}.name`}
                                    id={`${member}.name`} prepend={false} className="form__input"/>
                            </li>
                            
                            <li className="form__group">
                                <Field component={renderSelect} label={"Skill rating (out of 10)"} name={`${member}.proficiency`} 
                                    id={`${member}.proficiency`} className="form__input" prepend={false}>
                                    <option value="">Choose</option>
                                    <option value="1" >1</option>
                                    <option value="2" >2</option>
                                    <option value="3" >3</option>
                                    <option value="4" >4</option>
                                    <option value="5" >5</option>
                                    <option value="6" >6</option>
                                    <option value="7" >7</option>
                                    <option value="8" >8</option>
                                    <option value="9" >9</option>
                                    <option value="10">10</option>
                                </Field>
                            </li>
                        </ul>

                    </div>
            )})}
        </div>
    
    )
}

export default renderLanguage