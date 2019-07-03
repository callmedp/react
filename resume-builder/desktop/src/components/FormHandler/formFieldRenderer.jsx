import React from 'react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AsyncSelect from 'react-select/lib/Async';
import AsyncCreatableSelect from 'react-select/lib/AsyncCreatable';
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
                                iconClass,
                                autoFocus,
                                maxLength,
                                disabled,
                                meta: {touched, error, warning}
                            }) => {
    return (
        <React.Fragment>
            {index ?


                <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                    <input {...input} className={className}

                           onClick={(e) => tillTodayDisable(index, !input.checked, e)}
                           maxLength={maxLength} disabled={disabled}
                           autoComplete="off" placeholder={label} type={type}/>
                    {
                        !!(text) && <span>{text}</span>
                    }
                    {touched &&
                    ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                        (warning && <span className={'Warn-Message'}>{warning}</span>))}
                </div>
                :
                <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
                    <div className="input-group--input-group-icon">
                        <span className={iconClass}></span>
                    </div>
                    <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                        <input
                            {...input} disabled={disabled}
                            autoFocus={autoFocus} maxLength={maxLength}
                            className={className} autoComplete="off" placeholder={label} type={type}/>
                        {touched &&
                        ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                            (warning && <span className={'Warn-Message'}>{warning}</span>))}
                    </div>
                </div>

            }
        </React.Fragment>
    )
};


function handleMaxDate(maxDateAllowed, endDate, startDate, educationEndDate) {
    if (!maxDateAllowed) {
        return null;
    }
    if (!endDate) {
        if (educationEndDate && startDate) {
            const d1 = new Date(moment(startDate).add(5, 'years'))
            const d2 = new Date()
            return d1.getTime() >= d2.getTime() ? d1 : d2
        }
        return new Date()
    }
    return new Date(endDate)


}

export const datepicker =
    ({
         input,
         label,
         type,
         onDateChange,
         disabled,
         iconClass,
         maxDateAllowed,
         endDate = null,
         yearDropDownItemNumber,
         startDate = null,
         meta: {touched, error, warning},
         educationEndDate = false
     }) => (
        <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
            <div className="input-group--input-group-icon">
                <span className={iconClass}></span>
            </div>
            <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                <DatePicker {...input}
                            value={disabled ? moment().format('YYYY-MM-DD').toString() : input.value ? moment(input.value).format('YYYY-MM-DD').toString() : null}
                            dateFormat="yyyy-MM-dd"
                            autoComplete="off"
                            selected={input.value ? new Date(input.value) : null}
                            maxDate={handleMaxDate(maxDateAllowed, endDate, startDate, educationEndDate)}
                            minDate={startDate ? new Date((startDate)) : null}
                            onChange={date => input.onChange(date)}
                            showYearDropdown
                            withPortal
                            yearDropdownItemNumber={yearDropDownItemNumber}
                            scrollableYearDropdown
                            showMonthDropdown
                            disabled={disabled}
                            popperModifiers={{
                                offset: {
                                    enabled: true,
                                    offset: '5px, 10px'
                                },
                                preventOverflow: {
                                    enabled: true,
                                    escapeWithReference: false, // force popper to stay in viewport (even when input is scrolled out of view)
                                    boundariesElement: 'viewport'
                                }
                            }}
                />
                {touched &&
                ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                    (warning && <span className={'Warn-Message'}>{warning}</span>))}
            </div>
        </div>
    )

const selectStyles = {menu: styles => ({...styles, zIndex: 999})};


export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options,
                                 isMulti,
                                 iconClass,
                                 closeMenuOnSelect,
                                 selectBody = true,
                                 isSearchable = false

                             }) => (
    <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
        <div className="input-group--input-group-icon">
            <span className={iconClass}></span>
        </div>
        <div className={"Error " + (touched && error ? 'errormsg' : '')}>
            <Select {...input}
                    placeholder={label}
                    styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                    menuPortalTarget={selectBody ? document.body : document.getElementById('right-panel-section')}
                    options={options}
                    isMulti={isMulti}
                    closeMenuOnSelect={closeMenuOnSelect}
                    autoComplete="off"
                    isSearchable={isSearchable}
                    menuPosition={'absolute'}
                    menuPlacement={'auto'}
                    components={makeAnimated()}
                    onBlur={() => {
                        input.onBlur(input.value)
                    }}
            />
            {touched &&
            ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
);


export const renderDynamicSelect = ({
                                        input,
                                        loadOptions,
                                        label,
                                        defaultOptions,
                                        iconClass,
                                        isMulti,
                                        closeMenuOnSelect,
                                        meta: {touched, error, warning}
                                    }) => {
    return (
        <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
            <div className="input-group--input-group-icon">
                <span className={iconClass}></span>
            </div>
            <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                <AsyncSelect {...input}
                             loadOptions={loadOptions}
                             styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                             menuPortalTarget={document.getElementById('right-panel-section')}
                             menuPosition={'absolute'}
                             menuPlacement={'auto'}
                             defaultOptions={defaultOptions}
                             placeholder={label}
                             isMulti={isMulti}
                             autoComplete="off"
                             closeMenuOnSelect={closeMenuOnSelect}
                             onBlur={() => {
                                 input.onBlur(input.value)
                             }}
                />
                {touched &&
                ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                    (warning && <span className={'Warn-Message'}>{warning}</span>))}
            </div>
        </div>
    )
}


export const renderAsyncCreatableSelect = ({
                                               input,
                                               loadOptions,
                                               label,
                                               defaultOptions,
                                               iconClass,
                                               isMulti,
                                               closeMenuOnSelect,
                                               meta: {touched, error, warning},
                                               selectBody
                                           }) => {
    return (
        <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
            <div className="input-group--input-group-icon">
                <span className={iconClass}></span>
            </div>
            <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                <AsyncCreatableSelect {...input}
                                      cacheOptions
                                      loadOptions={loadOptions}
                                      styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                                      menuPortalTarget={selectBody ? document.body : document.getElementById('right-panel-section')}
                                      menuPosition={'absolute'}
                                      menuPlacement={'auto'}
                                      defaultOptions={defaultOptions}
                                      placeholder={label}
                                      isMulti={isMulti}
                                      autoComplete="off"
                                      closeMenuOnSelect={closeMenuOnSelect}

                                      onBlur={() => {
                                          input.onBlur(input.value)
                                      }}
                />
                {touched &&
                ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                    (warning && <span className={'Warn-Message'}>{warning}</span>))}
            </div>
        </div>
    )
}

export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   rows,
                                   iconClass,
                                   noIcon,
                                   showWordCounter = true,
                                   maxLength,
                                   meta: {touched, error, warning}

                               }) => (
    <React.Fragment>
        {noIcon ?
            <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                <textarea {...input}
                          autoComplete="off"
                          placeholder={label}
                          maxLength={maxLength}
                          rows={rows} type={type}/>
                {
                    showWordCounter &&
                    <span
                        className="word-counter mt-5">{input.value.length ? input.value.length : 0}/{maxLength}</span>
                }
                {touched &&
                ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                    (warning && <span className={'Warn-Message'}>{warning}</span>))}
            </div>
            :
            <div className={"input-group " + (touched && error ? 'errormsg' : '')}>
                <div className="input-group--input-group-icon">
                    <span className={iconClass}></span>
                </div>
                <div className={"Error " + (touched && error ? 'errormsg' : '')}>
                        <textarea {...input}
                                  autoComplete="off"
                                  placeholder={label}
                                  maxLength={maxLength}
                                  rows={rows} type={type}/>
                    {

                        showWordCounter && <span
                            className="word-counter mt-5">{input.value.length ? input.value.length : 0}/{maxLength}</span>
                    }

                    {touched &&
                    ((error && <span className={'errormsg-txt'}>{error}</span>) ||
                        (warning && <span className={'Warn-Message'}>{warning}</span>))}
                </div>
            </div>
        }

    </React.Fragment>
)


export const feedbackRenderField = ({
                                        input,
                                        label,
                                        type,
                                        className,
                                        meta: {touched, error, warning}
                                    }) => {
    return (
        <React.Fragment>
            {
                <div className="feedback-input">
                    <div className={(touched && error ? "fedback-input-error" : '')}>
                        <input {...input}
                               className={className}
                               autoComplete="off"
                               placeholder={label}
                               type={type}/>
                    </div>
                    <div>
                        {touched && ((error && <span className={'error-feedback'}>{error}</span>))}
                    </div>
                </div>
            }
        </React.Fragment>
    )
};





