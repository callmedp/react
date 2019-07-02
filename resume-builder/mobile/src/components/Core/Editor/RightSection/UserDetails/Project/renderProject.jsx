import React from 'react';
import {Field} from "redux-form";
import {
    datepicker,
    renderField,
    renderTextArea,
    renderCheckboxField
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {projectNewData} from "../../../../../../Utils/addnewData"

const renderProjects = ({
                            fields,
                            meta: {touched, error, submitFailed},
                            handleSubmit,
                            handleAddition,
                                eventClicked,
                            deleteProject,
                            changeOrderingUp,
                            changeOrderingDown,
                            editHeading,
                            heading,
                            headingChange,
                            editHeadingClick,
                            context,
                            till_today,
                            tillTodayDisable,
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
                        </React.Fragment> :
                        <React.Fragment>
                            <input type="text" autoFocus defaultValue={heading} maxLength={'20'}
                                   onChange={(event) => context.setState({heading: event.target.value})}/>
                            <i className="sprite icon--editTick"
                               onClick={() => {
                                   headingChange(entity_preference_data, heading, 3);
                                   context.setState({editHeading: false})
                               }}></i>
                        </React.Fragment>
                    }
                </div>
                {!editHeading ?
                    <button role="button" className="btn btn__round btn--outline"
                            onClick={handleSubmit(handleAddition.bind(this, fields, projectNewData(fields), 200, 'project',eventClicked,'Projects'))}
                            type={'button'}>+ Add new</button> : ''
                }
            </div>
            {fields.map((member, index) => {
                return (
                    <div className="form-wrap" key={index} id={`project${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).project_name || 'Project'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span
                                        className={"sprite icon--delete " + (fields.length === 1 && !fields.get(index).id ? "hide" : "")}
                                        onClick={(event) => deleteProject(index, fields, event)}
                                        role="button"></span>
                                </li>
                                {index === 0 ? '' :
                                    <li className="subHeading__btn"
                                        onClick={(event) => {
                                            fields = changeOrderingUp(index, fields, event);
                                            context.setState({fields})
                                        }}>
                                        <i className="sprite icon--upArrow"></i>
                                    </li>
                                }
                                {index === fields.length - 1 ? '' :
                                    <li className="subHeading__btn"
                                        onClick={(event) => {
                                            fields = changeOrderingDown(index, fields, event);
                                            context.setState({fields})
                                        }}>
                                        <i className="sprite icon--downArrow"></i>
                                    </li>
                                }
                            </ul>
                        </div>

                        <ul className="form pb-0">

                            <li className="form__group">
                                <Field component={renderField} label={"Project name"} type={"text"}
                                       name={`${member}.project_name`} prepend={true}
                                       id={`${member}.project_name`} iconClass={"sprite icon--project-gray"}
                                       className="form__input" maxLength={'50'}/>
                            </li>

                            <li className="form__group dob">
                                <Field component={datepicker} label={"Date from"}
                                       maxDateAllowed={true}
                                       endDate={fields.get(index).end_date || null}
                                       type={"date"} yearDropDownItemNumber={15}
                                       name={`${member}.start_date`} id={`${member}.start_date`}/>
                            </li>

                            <li className="form__group dob">
                                <Field component={datepicker} label={"Date to"} type={"date"}
                                       minDate={fields.get(index).start_date}
                                       startDate={fields.get(index).start_date || null}
                                       maxDateAllowed={true}
                                       yearDropDownItemNumber={15} name={`${member}.end_date`} id={`${member}.end_date`}
                                       disabled={till_today[index]}/>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <Field type="checkbox" name={`${member}.currently_working`}
                                       component={renderCheckboxField}
                                       className="form__radio-input" id={`${member}.currently_working`}
                                       tillTodayDisable={tillTodayDisable}
                                       index={`${index}`}/>
                                <label className="form__radio-label" htmlFor={`${member}.currently_working`}>
                                    <span className="form__radio-button"></span>
                                    Till today
                                </label>

                            </li>

                            <li className="form__group">
                                <Field component={renderTextArea} rows={"3"} type={"textarea"}
                                       className="form__input" name={`${member}.description`}
                                       prepend={true} iconClass={"sprite icon--description"} label={'Description'}
                                       value={`${member}.description`} maxLength={'300'}/>
                            </li>
                        </ul>
                    </div>
                )
            })}
        </div>

    )
}

export default renderProjects