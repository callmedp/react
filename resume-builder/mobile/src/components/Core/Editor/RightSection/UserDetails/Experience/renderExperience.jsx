import React from 'react';
import {
    renderField,
    renderTextArea,
    datepicker,
    renderCheckboxField,
    renderAsyncCreatableSelect
} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field} from 'redux-form';
import {experienceNewData} from "../../../../../../Utils/addnewData"
import {jobTitles} from "../../../../../../Utils/jobTitles";

const renderExperiences = ({
                               fields,
                               meta: {touched, error, submitFailed},
                               handleSubmit,
                               handleAddition,
                                eventClicked,
                               deleteExperience,
                               changeOrderingUp,
                               changeOrderingDown,
                               editHeading,
                               heading,
                               entity_preference_data,
                               editHeadingClick,
                               till_today,
                               context,
                               openModal,
                               tillTodayDisable,
                               fetchJobTitles,
                               headingChange,
                               showAlertMessage
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
                                   headingChange(entity_preference_data, heading, 2);
                                   context.setState({editHeading: false})
                               }}></i>
                        </React.Fragment>
                    }
                </div>
                {!editHeading ?
                    <button role="button"
                            onClick=
                            {
                        
                                handleSubmit((values) => {
                                    let skipAddition = false;
                                    (values && values.list || []).forEach(el => {
                                        if (!el.job_profile) {
                                            skipAddition = true;
                                        }
                                    })
                                    if (!skipAddition) {
                                        handleAddition(fields, experienceNewData(fields), 780, 'experience', eventClicked, 'Experience')
                                    }
                                    else {
                                        showAlertMessage()
                                    }
                                })}
                            type={'button'} className="btn btn__round btn--outline">+ Add new</button> : ''
                }
            </div>
            {fields.map((member, index) => {
                return (
                    <div className="form-wrap" key={index} id={`experience${index}`}>
                        <div className="subHeading pb-0">
                            <h2>{fields.get(index).company_name || 'Experience'}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                <span
                                    className={"sprite icon--delete " + (fields.length === 1 && !fields.get(index).id ? "hide" : "")}
                                    onClick={(event) => deleteExperience(index, fields, event)}
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

                            {/* <li className="form__group">
                            
                            <Field component={renderField} label={"Designation"}  type={"text"} name={`${member}.job_profile`} prepend={true} 
                                id={`${member}.job_profile`} iconClass={"sprite icon--designation"} className="form__input"/>
                        </li> */}

                            <li className="form__group">
                                <Field component={renderAsyncCreatableSelect} label={"Designation"}
                                       name={`${member}.job_profile`}
                                       id={`${member}.job_profile`}
                                       defaultOptions={jobTitles}

                                       iconClass={"sprite icon--designation"} className={'async-select'}

                                       closeMenuOnSelect={true} isMulti={false}
                                       loadOptions={(inputValue) => fetchJobTitles(inputValue, '')}
                                />
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Company name"} maxLength={'50'} type={"text"}
                                       name={`${member}.company_name`}
                                       id={`${member}.company_name`} iconClass={"sprite icon--company"}
                                       className="form__input" prepend={true} maxLength={'50'}/>
                            </li>

                            <li className="form__group dob">
                                <Field component={datepicker} label={"Date from"} type={"date"}
                                       yearDropDownItemNumber={15}
                                       maxDateAllowed={true}
                                       endDate={fields.get(index).end_date || null}
                                       name={`${member}.start_date`} id={`${member}.start_date`}/>
                            </li>

                            <li className="form__group dob">
                                <Field component={datepicker}
                                       label={"Date to"} type={"date"}
                                       minDate={fields.get(index).start_date}
                                       maxDateAllowed={true}
                                       startDate={fields.get(index).start_date || null}
                                       yearDropDownItemNumber={15}
                                       name={`${member}.end_date`} id={`${member}.end_date`}
                                       disabled={till_today[index]}/>
                            </li>

                            <li className="form__radio-group d-flex justify-content-end fs-14">
                                <Field type="checkbox" name={`${member}.is_working`} component={renderCheckboxField}
                                       className="form__radio-input" id={`${member}.is_working`}
                                       tillTodayDisable={tillTodayDisable}
                                       index={`${index}`}/>
                                <label className="form__radio-label" htmlFor={`${member}.is_working`}>
                                    <span className="form__radio-button"></span>
                                    Till today
                                </label>

                            </li>

                            <li className="form__group">
                                <Field component={renderField} maxLength={'50'} label={"Job Location"} type={"text"}
                                       name={`${member}.job_location`}
                                       id={`${member}.job_location`} iconClass={"sprite icon--location"}
                                       className="form__input" prepend={true}/>
                            </li>

                            <li className="form__group">
                                <Field component={renderTextArea} type={"textarea"} name={`${member}.work_description`}
                                       label={'Description'}
                                       className="form__input h-150" rows="5" maxLength={'1000'}
                                       id={`${member}.work_description`}
                                />
                                <p className="add-suggested" onClick={event => {
                                    event.preventDefault();
                                    openModal(fields, index)
                                }}>
                                    <span>+</span>Add suggested Description
                                </p>
                            </li>


                        </ul>
                    </div>
                )
            })}

        </div>

    )
}

export default renderExperiences;