import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from 'moment';

export const required = value => value ? undefined : 'Required';

export const email = value =>
    value && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)
        ? 'Invalid email address'
        : undefined;

export const phoneNumber = value =>
    value && !/^(0|[1-9][0-9]{9})$/i.test(value)
        ? 'Invalid phone number, must be 10 digits'
        : undefined;


export const renderField = ({
                                input,
                                label,
                                type,
                                meta: {touched, error, warning}
                            }) => (
    <div>
        <label>{label}</label>
        <div className={'Top-space'}>
            <input {...input} placeholder={label} type={type}/>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
)


export const datePicker = ({
                               input,
                               label,
                               type,
                               meta: {touched, error, warning}
                           }) => (
    <div>
        <label>{label}</label>
        <div className={'Top-space'}>
            <DatePicker {...input} dateForm="MM/DD/YYYY" placeholder={label}
                        selected={input.value ? moment(input.value) : null}/>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
)

export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 children
                             }) => (
    <div>
        <label>{label}</label>
        <div className={'Top-space'}>
            <select {...input} >
                {children}
            </select>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
)

export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   meta: {touched, error, warning}

                               }) => (
    <div>
        <label>{label}</label>
        <div className={'Top-space'}>
            <textarea {...input} placeholder={label} type={type}/>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>

)

