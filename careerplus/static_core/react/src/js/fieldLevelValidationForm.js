import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from 'moment';
import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';


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
        <div className={'Top-space'}>
            <input {...input} className={'Field-spacing'} placeholder={label} type={type}/>
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
                               onDateChange,
                               meta: {touched, error, warning}
                           }) => (
    <div>
        <div className={'Top-space'}>
            <DatePicker {...input} dateFormat="yyyy-MM-dd" placeholderText={label} className="Field-spacing"
                        selected={input.value ? moment(input.value).format("YYYY-MM-DD") : null}
                        onChange={date => input.onChange(moment(date).format("YYYY-MM-DD"))}
            />
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
                                 options
                             }) => (
    <div>
        <div className={'Top-space'}>
            <Select {...input}
                    placeholder={label}
                    options={options}
                    onBlur={() => {
                        input.onBlur(input.value)
                    }}
            />
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
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
    <div>
        <div className={'Top-space'}>
            <textarea {...input} placeholder={label} type={type}/>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>

)

