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
<<<<<<< HEAD
<div className="Error">
    <input {...input} className={className} placeholder={label} type={type}/>
     {
    (( <span className={'Error-message'}>{error}</span>) ||
         (warning && <span className={'Warn-Message'}>{warning}</span>))}
</div>
=======
    <div>
        <input {...input} className={className} placeholder={label} type={type}/>
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>
>>>>>>> abc6c107d1bb7a10236d8dc48c0db2c0bad55159
);


export const datepicker =
    ({
         input,
         label,
         type,
         onDateChange,
         meta: {touched, error, warning}
     }) => (
        <div>
            <DatePicker {...input} dateFormat="yyyy-MM-dd"
                        selected={input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)}


            />
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    )


export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options,
                                 isMulti
                             }) => (
    <div>
        <Select {...input}
                placeholder={label}
                options={options}
                isMulti={isMulti}
                onBlur={() => {
                    input.onBlur(input.value)
                }}
        />
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>
);


export const renderDynamicSelect = ({
                                        input,
                                        loadOptions,
                                        label,
                                        defaultOptions,
                                        meta: {touched, error, warning}
                                    }) => (
    <div>
        <AsyncSelect {...input}
                     loadOptions={loadOptions}
                     defaultOptions={defaultOptions}
                     placeholder={label}
                     isMulti={true}
                     onBlur={() => {
                         input.onBlur(input.value)
                     }}
        />
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>
)

export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   meta: {touched, error, warning}

                               }) => (
    <div>
        <textarea {...input} placeholder={label} type={type}/>
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>


)

