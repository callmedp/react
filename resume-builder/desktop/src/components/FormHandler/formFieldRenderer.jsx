import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';
import makeAnimated from 'react-select/lib/animated'


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                tillTodayDisable,
                                index,
                                meta: {touched, error, warning}
                            }) => {
    return (
        <React.Fragment>
            {index ?
                <div className="Error">
                    <input {...input} className={className} onClick={(e)=>tillTodayDisable(index,!input.checked,e)} autoComplete="off" placeholder={label} type={type}/>
                    {touched &&
                    ((error && <span className={'Error-message'}>{error}</span>) ||
                        (warning && <span className={'Warn-Message'}>{warning}</span>))}
                </div>:
                <div className="Error">
                    <input {...input} className={className} autoComplete="off" placeholder={label} type={type}/>
                    {touched &&
                    ((error && <span className={'Error-message'}>{error}</span>) ||
                        (warning && <span className={'Warn-Message'}>{warning}</span>))}
                </div>
            }
        </React.Fragment>
    )
};


export const datepicker =
    ({
         input,
         label,
         type,
         onDateChange,
         disabled,
         meta: {touched, error, warning}
     }) => (
        <div className="Error">
            <DatePicker {...input}
                        dateFormat="yyyy-MM-dd"
                        autoComplete="off"
                        selected={input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)}
                        showYearDropdown
                        yearDropdownItemNumber={20}
                        scrollableYearDropdown
                        showMonthDropdown
                        disabled={disabled}


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
    <div className="Error">
        <Select {...input}
                placeholder={label}
                options={options}
                isMulti={isMulti}
                closeMenuOnSelect={false}
                autoComplete="off"
                components={makeAnimated()}
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
    <div className="Error">
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

                                   meta: {touched, error, warning}

                               }) => (
    <div className="Error">
        <textarea {...input} placeholder={label} rows={rows} type={type}/>
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>


)

