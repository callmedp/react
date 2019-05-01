import React from 'react';
import {Field} from "redux-form"
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";


const renderSkills = ({
                        fields, 
                        meta: {touched, error, submitFailed},
                        handleSubmit,
                        handleAddition,
                        deleteSkill,
                        changeOrderingUp,
                        changeOrderingDown,
                        editHeading,
                        heading,
                        updateInputValue,
                        editHeadingClick
                    }) => {
    return (
        <React.Fragment>
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading heading">
                    <div className="heading__info">
                        {!editHeading ?
                            <h1>{heading}</h1>:
                            <input type="text" autoFocus placeholder={heading} onBlur={(e)=>updateInputValue('blur',e)}
                            onKeyDown={(e)=>updateInputValue('keyPress',e)}/>
                        }
                        <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                    </div>
                    <button type={'button'} onClick={handleSubmit(handleAddition.bind(this,fields))} 
                        className="btn btn__round btn--outline">+ Add new</button>
                </div>
            
            {fields.map((member, index) => {
                return(
                    <div className="form-wrap" key={index} id={`skill${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).name || 'Skill'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span onClick={(event) => deleteSkill(index, fields, event)}
                                     className={"sprite icon--delete " +(fields.get(index).id ? "":"hide")} role="button"></span>
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
                                <Field component={renderField} label={"Skill name"}  type={"text"} name={`${member}.name`}
                                    id={`${member}.name`} iconClass={"sprite icon--skills-grey"} className="form__input" prepend={true}/>
                            </li>

                            <li className="form__group">
                                <Field component={renderSelect} label={"Skill rating (out of 10)"} name={`${member}.proficiency`} 
                                    id={`${member}.proficiency`} className="form__select" prepend={false}>
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
            {error && <li>{error}</li>}
            </div>
     
        </React.Fragment>         
    )
}

export default renderSkills