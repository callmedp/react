import React from 'react';
import { Field } from "redux-form"
import { renderField, renderSelect } from "../../../../../FormHandler/formFieldRenderer.jsx";
import { skillNewData } from "../../../../../../Utils/addnewData"


const renderSkills = ({
    fields,
    meta: { touched, error, submitFailed },
    handleSubmit,
    handleAddition,
    eventClicked,
    deleteSkill,
    changeOrderingUp,
    changeOrderingDown,
    editHeading,
    heading,
    headingChange,
    context,
    editHeadingClick,
    entity_preference_data,
    showAlertMessage,
    sendTrackingInfo
}) => {
    return (
        <React.Fragment>
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading heading">
                    <div className="heading__info">
                        {!editHeading ?
                            <React.Fragment>
                                <h1 className="heading-style">{heading}</h1>
                                <i className="sprite icon--edit" onClick={editHeadingClick.bind(true)}></i>
                            </React.Fragment> :
                            <React.Fragment>
                                <input type="text" autoFocus defaultValue={heading} maxLength={'20'}
                                    onChange={(event) => context.setState({ heading: event.target.value })} />
                                <i className="sprite icon--editTick"
                                    onClick={() => { headingChange(entity_preference_data, heading, 4); context.setState({ editHeading: false }) }}></i>
                            </React.Fragment>
                        }
                    </div>
                    {!editHeading ?
                        <button type={'button'} onClick={
                            handleSubmit((values) => {
                                let skipAddition = false;
                                (values && values.list || []).forEach(el => {
                                    if (!el.name) {
                                        skipAddition = true;
                                    }
                                })
                                if (!skipAddition) {
                                    sendTrackingInfo('right_section_add',1)
                                    handleAddition(fields, skillNewData(fields), 0, 'skill', eventClicked, 'Skills')
                                }
                                else {
                                    showAlertMessage()
                                }
                            })}
                            className="btn btn__round btn--outline">+ Add new</button> : ''
                    }
                </div>

                {fields.map((member, index) => {
                    return (
                        <div className="form-wrap" key={index} id={`skill${index}`}>
                            <div className="subHeading pb-0">
                                <h2>{fields.get(index).name || 'Skill'}</h2>
                                <ul className="subHeading__control">
                                    <li className="subHeading__delete">
                                        <span onClick={(event) => deleteSkill(index, fields, event)}
                                            className={"sprite icon--delete " + (fields.length === 1 && !fields.get(index).id ? "hide" : "")} role="button"></span>
                                    </li>
                                    {index === 0 ? '' :
                                        <li className="subHeading__btn"
                                            onClick={(event) => { fields = changeOrderingUp(index, fields, event); context.setState({ fields }) }}>
                                            <i className="sprite icon--upArrow"></i>
                                        </li>
                                    }
                                    {index === fields.length - 1 ? '' :
                                        <li className="subHeading__btn"
                                            onClick={(event) => { fields = changeOrderingDown(index, fields, event); context.setState({ fields }) }}>
                                            <i className="sprite icon--downArrow"></i>
                                        </li>
                                    }
                                </ul>
                            </div>

                            <ul className="form pb-0">

                                <li className="form__group">
                                    <Field component={renderField} label={"Skill name"} type={"text"} name={`${member}.name`} maxLength={'50'}
                                        id={`${member}.name`} iconClass={"sprite icon--skills-grey"} className="form__input" prepend={true} />
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
                    )
                })}
            </div>

        </React.Fragment>
    )
}

export default renderSkills;