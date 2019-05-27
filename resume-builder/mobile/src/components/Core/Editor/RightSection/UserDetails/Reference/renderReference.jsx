import React from 'react';
import {Field} from "redux-form";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import DataLoader from "../../../../../Common/DataLoader/dataloader"
import {referenceNewData} from "../../../../../../Utils/addnewData"

const renderReferences = ({
                            fields, 
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            handleAddition,
                            deleteReference,
                            changeOrderingUp,
                            changeOrderingDown,
                            editHeading,
                            heading,
                            updateInputValue,
                            editHeadingClick,
                            loader
                        }) => {
    return (
        
        <div className="buildResume__wrap">
                {loader ? <DataLoader/> :""}
            <div className="buildResume__heading heading">
                <div className="heading__info">
                {!editHeading ?
                        <React.Fragment>
                            <h1>{heading}</h1>
                            <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                        </React.Fragment>:
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} onBlur={(e)=>updateInputValue('blur',e)}
                                onKeyDown={(e)=>updateInputValue('keyPress',e)}/>
                            <i className="sprite icon--editTick"></i>
                        </React.Fragment>
                    }
                </div>
                {!editHeading ?
                    <button role="button" className="btn btn__round btn--outline"
                        onClick={handleSubmit(handleAddition.bind(this,fields,referenceNewData(fields),150,'references'))}
                        type={'button'}>+ Add new</button>:''
                }
            </div>
            {fields.map((member, index) => {
                return (
                    <div className="form-wrap" key={index} id={`references${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).reference_name || 'Reference'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className={"sprite icon--delete " +(fields.length === 1 && !fields.get(index).id ? "hide":"")} role="button"
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
                                <Field component={renderField} label={"Reference name"}  type={"text"} name={`${member}.reference_name`} prepend={true}
                                    id={`${member}.reference_name`} iconClass={"sprite icon--project-gray"} className="form__input"/>
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Designation"}  type={"text"} name={`${member}.reference_designation`} prepend={true}
                                    id={`${member}.reference_designation`} iconClass={"sprite icon--designation"} className="form__input"/>
                            </li>
                            

                            <li className="form__group">
                                <label className="form__label" htmlFor="about_candidate">Description</label>
                                <Field component={renderTextArea} rows="3" type={"textarea"}
                                    className="form__input" name={`${member}.about_candidate`}/>
                            </li>
                            
                        </ul>
                    </div>
                )})}
        </div>

    )
}

export default renderReferences