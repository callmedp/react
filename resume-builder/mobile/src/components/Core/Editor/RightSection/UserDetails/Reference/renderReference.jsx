import React from 'react';
import {Field} from "redux-form";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";

const renderReferences = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleAddition,
                            deleteReference,
                            changeOrderingUp,
                            changeOrderingDown,
                        }) => {
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>References</h1>
                    <i className="sprite icon--edit"></i>
                </div>
                <button role="button" className="btn btn__round btn--outline"
                    onClick={handleAddition.bind(this, fields, error)}
                    type={'button'}>+ Add new</button>
            </div>
            {fields.map((member, index) => {
                return (
                    <React.Fragment key={index}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).reference_name || 'Refrence'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" role="button"
                                    onClick={(event) => deleteReference(index, fields, event)}></span>
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
                                <label className="form__label" htmlFor="reference_name">Reference name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--project-gray"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} type={"text"} className="form__input"
                                        name={`${member}.reference_name`}/>
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" htmlFor="reference_designation">Designation</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--designation"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} type={"text"} 
                                        name={`${member}.reference_designation`} className="form__input"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="about_candidate">Description</label>
                                <Field component={renderTextArea} rows="3" type={"textarea"}
                                    className="form__input" name={`${member}.about_candidate`}/>
                            </li>
                            
                        </ul>
                    </React.Fragment>
                )})}
        </div>

    )
}

export default renderReferences