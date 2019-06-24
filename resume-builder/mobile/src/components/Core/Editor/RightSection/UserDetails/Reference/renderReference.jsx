import React from 'react';
import {Field} from "redux-form";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
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
                            headingChange,
                            editHeadingClick,
                            context,
                            entity_preference_data
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
                                onClick={()=>{headingChange(entity_preference_data,heading,9);context.setState({editHeading:false})}}></i>
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
                                <Field component={renderField} label={"Reference name"}  type={"text"} name={`${member}.reference_name`} prepend={true}
                                    id={`${member}.reference_name`} iconClass={"sprite icon--project-gray"} className="form__input" maxLength={'50'}/>
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Designation"}  type={"text"} name={`${member}.reference_designation`} prepend={true}
                                    id={`${member}.reference_designation`} iconClass={"sprite icon--designation"} className="form__input" maxLength={'50'}/>
                            </li>
                            

                            <li className="form__group">
                                <Field component={renderTextArea} rows="3" type={"textarea"} label={'Description'} id={`${member}.about_candidate`}
                                    className="form__input" name={`${member}.about_candidate`} maxLength={'300'}/>
                            </li>
                            
                        </ul>
                    </div>
                )})}
        </div>

    )
}

export default renderReferences