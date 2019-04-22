import React from 'react';
import {Field} from "redux-form";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";

const renderCourse = ({
                        fields, 
                        meta: {touched, error, submitFailed},
                        handleAddition,
                        deleteCourse,
                        changeOrderingUp,
                        changeOrderingDown,}) => 
{
    return (
        
        <div className="buildResume__wrap">
            <div className="buildResume__heading heading">
                <div className="heading__info">
                    <h1>Courses</h1>
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
                        <h2>{fields.get(index).name_of_certification || 'New Course'}</h2>
                        <ul className="subHeading__control">
                            <li className="subHeading__delete">
                                <span className="sprite icon--delete" 
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
                            <label className="form__label" htmlFor="name_of_certification">Course name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--course-grey"></i>
                                    </span>
                                </div>
                                <Field component={renderField} className="form__input"
                                    type={"text"} name={`${member}.name_of_certification`}/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="year_of_certification">Completion Year</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--date"></i>
                                    </span>
                                </div>
                                <Field component={datepicker} type={"date"} 
                                name={`${member}.year_of_certification`} className="form__input" />
                            </div>
                        </li>
                    </ul>
                </React.Fragment>
            )})}
        </div>

    )
}

export default renderCourse