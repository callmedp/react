import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                meta: {touched, error, warning}
                            }) => (
        <React.Fragment>
            <input {...input} className={className} placeholder={label} type={type}/>
            <div className="Error">
            {touched &&
                ((<span className={'Error-message'}>{error}</span>) ||
                    (warning && <span className={'Warn-Message'}>{warning}</span>))
            }
            </div>
        </React.Fragment>
);


export const datepicker =
    ({
         input,
         label,
         className,
         type,
         onDateChange,
         meta: {touched, error, warning}
     }) => (
        <React.Fragment>
            <DatePicker {...input} dateFormat="yyyy-MM-dd" className={className}
                        selected={input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)}
            />
            <div className="Error">
            {  ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
            </div>
        </React.Fragment>
    )


export const renderSelect = ({
                                 input,
                                 name,
                                 label,
                                 meta: {touched, error, warning},
                                 options,
                                 className,
                                 isMulti
                             }) => (
    <React.Fragment>
        <Select {...input}
                placeholder={label}
                name={name}
                options={options}
                className={className}
                isMulti={isMulti}
                value={input.value.label}
                onChange={(value) => input.onChange(value)}
                onBlur={() => {
                    input.onBlur(input.value)
                }}
        />
        <div>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </React.Fragment>
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
                                   rows,
                                   className,
                                   meta: {touched, error, warning}

                               }) => (
    <React.Fragment>
        <textarea {...input} placeholder={label} type={type} className={className} rows={rows}/>
        <div>
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </React.Fragment>


)

