import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from 'moment';
// import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';


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

export const datePicker = ({
                               input,
                               label,
                               type,
                               onDateChange,
                               meta: {touched, error, warning}
                           }) => (
    <DatePicker {...input} dateFormat="yyyy-MM-dd"
                selected={input.value ? moment(input.value).format("YYYY-MM-DD") : null}
                onChange={date => input.onChange(moment(date).format("YYYY-MM-DD"))}
    />
)

export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options
                             }) => (
    <Select {...input}
            placeholder={label}
            options={options}
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

//
// export const renderDynamicSelect = ({
//                                         input,
//                                         loadOptions,
//                                         label,
//                                         defaultOptions
//                                     }) => (
//     <AsyncSelect {...input}
//                  loadOptions={loadOptions}
//                  defaultOptions={defaultOptions}
//                  placeholder={label}
//                  isMulti={true}
//                  onBlur={() => {
//                      input.onBlur(input.value)
//                  }}
//     />
// )

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

