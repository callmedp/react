import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from 'moment';
import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';
import PropTypes from 'prop-types';


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                meta: {touched, error, warning}
                            }) => (

    <input {...input} className={className} placeholder={label} type={type}/>
    // {touched &&
    // ((error && <span className={'Error-message'}>{error}</span>) ||
    //     (warning && <span className={'Warn-Message'}>{warning}</span>))}
);


export const datepicker =
    ({
         input,
         label,
         type,
         onDateChange,
         meta: {touched, error, warning}
     }) => (
        <DatePicker {...input} dateFormat="yyyy-MM-dd"
                    selected={input.value ? new Date(input.value) : null}
                    onChange={date => input.onChange(date)}


        />)


export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options,
                                 isMulti
                             }) => (
    <Select {...input}
            placeholder={label}
            options={options}
            isMulti={isMulti}
            onBlur={() => {
                input.onBlur(input.value)
            }}
    />
);

const adaptFileEventToValue = delegate => e => delegate(e.target.files[0]);

export const renderFileInput = ({
                                    input: {value: omitValue, onChange, onBlur, ...inputProps},
                                    meta: omitMeta,
                                    ...props
                                }) => {
    return (
        <input
            onChange={adaptFileEventToValue(onChange)}
            onBlur={adaptFileEventToValue(onBlur)}
            type="file"
            {...props.input}
            {...props}
        />
    );
};


export const renderDynamicSelect = ({
                                        input,
                                        loadOptions,
                                        label,
                                        defaultOptions
                                    }) => (
    <AsyncSelect {...input}
                 loadOptions={loadOptions}
                 defaultOptions={defaultOptions}
                 placeholder={label}
                 isMulti={true}
                 onBlur={() => {
                     input.onBlur(input.value)
                 }}
    />
)

export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   meta: {touched, error, warning}

                               }) => (

    <textarea {...input} placeholder={label} type={type}/>
    // {touched &&
    // ((error && <span className={'Error-message'}>{error}</span>) ||
    //     (warning && <span className={'Warn-Message'}>{warning}</span>))}


)

