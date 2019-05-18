import React from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';
import makeAnimated from 'react-select/lib/animated';
import moment from 'moment';

export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                tillTodayDisable,
                                index,
                                text,
                                meta: {touched, error, warning}
                            }) => {
    return (
        <React.Fragment>
            {index ?
                <div className="Error">
                    <input {...input} className={className} onClick={(e) => tillTodayDisable(index, !input.checked, e)}
                           autoComplete="off" placeholder={label} type={type}/>
                    {
                        !!(text) && <span>{text}</span>
                    }
                    {touched &&
                    ((error && <span className={'Error-message'}>{error}</span>) ||
                        (warning && <span className={'Warn-Message'}>{warning}</span>))}
                </div> :
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
         maxDateAllowed,
         yearDropDownItemNumber,
         meta: {touched, error, warning}
     }) => (
        <div className="Error">
            <DatePicker {...input}
                        value={disabled ? "This is disabled" : input.value}
                        dateFormat="yyyy-MM-dd"
                        autoComplete="off"
                        selected={input.value ? new Date(input.value) : null}
                        maxDate={maxDateAllowed ? new Date() : null}
                // minDate={dateValue !== ''  ? moment(dateValue).add(1, 'days') : null}
                        onChange={date => input.onChange(date)}
                        showYearDropdown
                        yearDropdownItemNumber={yearDropDownItemNumber}
                        scrollableYearDropdown
                        showMonthDropdown
                        disabled={disabled}

            />
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    )

const selectStyles = {menu: styles => ({...styles, zIndex: 999})};


export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options,
                                 isMulti,
                                 closeMenuOnSelect
                             }) => (
    <div className="Error">
        <Select {...input}
                placeholder={label}
                styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                menuPortalTarget={document.body}
                options={options}
                isMulti={isMulti}
                closeMenuOnSelect={closeMenuOnSelect}
                autoComplete="off"
                menuPosition={'absolute'}
                menuPlacement={'auto'}
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
                                        closeMenuOnSelect,
                                        meta: {touched, error, warning}
                                    }) => (
    <div className="Error">
        <AsyncSelect {...input}
                     loadOptions={loadOptions}
                     styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                     menuPortalTarget={document.getElementById('right-panel-section')}
                     menuPosition={'absolute'}
                     menuPlacement={'auto'}
                     defaultOptions={defaultOptions}
                     placeholder={label}
                     isMulti={true}
                     autoComplete="off"
                     closeMenuOnSelect={closeMenuOnSelect}
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
        <textarea {...input}
                  autoComplete="off"
                  placeholder={label}
                  rows={rows} type={type}/>
        {touched &&
        ((error && <span className={'Error-message'}>{error}</span>) ||
            (warning && <span className={'Warn-Message'}>{warning}</span>))}
    </div>


)

