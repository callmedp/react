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
                    <React.Fragment key={index}>
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
                                <label className="form__label" htmlFor="name">Language name</label>
                                <Field component={renderField} type={"text"} 
                                name={`${member}.name`} className="form__input"/>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" htmlFor="proficiency">Skill rating (out of 10)</label>
                                <Field name={`${member}.proficiency`}
                                            component={renderSelect}
                                            className="form__select"
                                            isMulti={false}
                                            options={[
                                                {value: 1, label: '1'},
                                                {value: 2, label: '2'},
                                                {value: 3, label: '3'},
                                                {value: 4, label: '4'},
                                                {value: 5, label: '5'},
                                                {value: 6, label: '6'},
                                                {value: 7, label: '7'},
                                                {value: 8, label: '8'},
                                                {value: 9, label: '9'},
                                                {value: 10, label: '10'}
                                            ]}
                                           />
                            </li>
                        </ul>

                    </React.Fragment>
            )})}
        </div>
    
    )
}

export default renderLanguage