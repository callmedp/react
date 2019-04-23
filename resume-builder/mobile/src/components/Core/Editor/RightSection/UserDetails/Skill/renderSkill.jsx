import React from 'react';
import {Field} from "redux-form"
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";


const renderSkills = ({
                        fields, 
                        meta: {touched, error, submitFailed},
                        handleAddition,
                        deleteSkill,
                        changeOrderingUp,
                        changeOrderingDown,
                    }) => {
    return (
        <React.Fragment>
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading heading">
                    <div className="heading__info">
                        <h1>Skills</h1>
                        <i className="sprite icon--edit"></i>
                    </div>
                    <button type={'button'} onClick={handleAddition.bind(this, fields, error)} 
                        className="btn btn__round btn--outline">+ Add new</button>
                </div>
            
            {fields.map((member, index) => {
                return(
                    <div className="form-wrap" key={index}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).name || 'Skill'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span onClick={(event) => deleteSkill(index, fields, event)}
                                     className="sprite icon--delete" role="button"></span>
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
                                <label className="form__label" htmlFor="name">Skill name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--skills-grey"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField}  type={"text"} name={`${member}.name`}
                                        className="form__input"/>
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" htmlFor="proficiency">Skill rating (out of 10)</label>
                                <Field name={`${member}.proficiency`} component={renderSelect} 
                                        className="form__select">
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