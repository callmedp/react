import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Multiselect from 'react-widgets/lib/Multiselect'
import moment from 'moment'
import addDays from "date-fns/addDays";
import AsyncCreatableSelect from 'react-select/lib/AsyncCreatable';


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                iconClass,
                                id,
                                prepend,
                                maxLength,
                                disabled,
                                meta: {touched, error, warning}
                            }) => (


    <React.Fragment>
        <label className="form__label" htmlFor={input.name}>{label}</label>
        {!prepend ?
            <React.Fragment>
                <input {...input} className={className + (touched && error ? " error error-field" : "")}
                       maxLength={maxLength} id={id} type={type} autoComplete="off" disabled={disabled}/>
                {touched &&
                ((<span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))
                }
            </React.Fragment> :

            <div className={"input-group " + (touched && error ? "error" : "")}>
                <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
                </div>
                <input {...input} className={className} id={id} type={type} maxLength={maxLength} autoComplete="off" disabled={disabled}/>
                {touched &&
                ((<span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))
                }

            </div>
        }
    </React.Fragment>
);

export const renderCheckboxField = ({
                                        input,
                                        type,
                                        className,
                                        id,
                                        tillTodayDisable,
                                        index
                                    }) => (


    <React.Fragment>
        <input {...input} className={className} onClick={(e) => tillTodayDisable(index, !input.checked, e)} id={id}
               type={type}/>
    </React.Fragment>
);

const Input = ({onChange, placeholder, value, id, onClick, name, disabled}) => (
    <input
        onChange={onChange}
        placeholder={placeholder}
        value={value}
        name={name}
        id={id}
        onClick={onClick}
        disabled={disabled}
        autoComplete="off"
        readOnly={true}
    />
);


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
         className,
         id,
         disabled,
         minDate,
         yearDropDownItemNumber,
         meta: {touched, error, warning},
         maxDateAllowed,
         educationEndDate = false,
         startDate = null,
         endDate = null,

     }) => (
        <React.Fragment>
            <label className="form__label" htmlFor={input.name}>{label}</label>
            <div className={"input-group " + (touched && error ? "error" : "")}>
                <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className="sprite icon--date"></i>
                    </span>
                </div>
                <DatePicker 
                            customInput={<Input id={id} name={input.name} disabled={disabled}/>}
                            value={disabled ? moment().format('YYYY-MM-DD').toString() : input.value ? moment(input.value).format('YYYY-MM-DD').toString() : null}
                            className={className}
                            dateFormat="yyyy-MM-dd"
                            autoComplete="off"
                            selected={input.value ? new Date(input.value) : null}
                            id={id}
                            withPortal
                            onChange={date => input.onChange(date)}
                            showYearDropdown
                            yearDropdownItemNumber={yearDropDownItemNumber}
                            scrollableYearDropdown
                            showMonthDropdown
                            disabledKeyboardNavigation={true}
                            disabled={disabled}
                            disabledNavigation
                            maxDate={handleMaxDate(maxDateAllowed, endDate, startDate, educationEndDate)}
                            minDate={startDate ? new Date((startDate)) : null}
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
                {touched && ((error && <span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))}
            </div>

        </React.Fragment>
    )


export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 children,
                                 className,
                                 iconClass,
                                 prepend
                             }) => (
    <React.Fragment>
        <label className="form__label" htmlFor={input.name}>{label}</label>
        {prepend ?
            <div className={"input-group " + (touched && error ? "error" : "")}>
                <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
                </div>
                <select {...input}
                         className={className}
                         value={input.value}
                        onBlur={() => {
                            input.onBlur(input.value)
                        }}
                >
                    {children}
                </select>
                <div className="select-error">
                    {touched &&
                    ((error && <span className={'error-message'}>{error}</span>) ||
                        (warning && <span className={'warn-Message'}>{warning}</span>))}
                </div>
            </div> :
            <React.Fragment>


                <select {...input} className={className + (touched && error ? " error error-field" : "")}
                        onBlur={() => {
                            input.onBlur(input.value)
                        }}
                >
                    {children}
                </select>
                {touched &&
                ((error && <span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))}
            </React.Fragment>
        }

    </React.Fragment>
);


export const renderMultiselect = ({input, className, data, valueField, textField, defaultValue}) => (

    <React.Fragment>
        <label className="form__label" htmlFor="extracurricular">Interest</label>
        <div className="input-group">

            <Multiselect {...input}
                         onBlur={() => input.onBlur()}
                         value={input.value.length ? input.value : defaultValue}
                         defaultValue={defaultValue}
                         data={data}
                         className={className}
                         valueField={valueField}
                         textField={textField}
                         placeholder={'Select Interest'}
            />

        </div>


    </React.Fragment>
)


export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   rows,
                                   id,
                                   className,
                                   iconClass,
                                   prepend,
                                   maxLength,
                                   meta: {touched, error, warning}

                               }) => (
    <React.Fragment>
        <label className="form__label" htmlFor={input.name}>{label}</label>
        {prepend ?
            <React.Fragment>
                <div className={"input-group " + (error ? "error" : "")}>
                    <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className={iconClass}></i>
                    </span>
                    </div>
                    <textarea {...input} placeholder={label} type={type} className={className} maxLength={maxLength}
                              rows={rows} id={id}/>
                    
                </div>
                <div>
                        {
                        ((error && <span className={'error-message'}>{error}</span>) ||
                            (warning && <span className={'warn-Message'}>{warning}</span>))}
                    </div>
                <p className="text-length">{input.value.length ? input.value.length : 0}- {maxLength}</p>
            </React.Fragment> :
            <React.Fragment>
                <textarea {...input} placeholder={label} type={type} className={className} maxLength={maxLength}
                          rows={rows} id={id}/>
                <div>
                    {touched &&
                    ((error && <span className={'error-message'}>{error}</span>) ||
                        (warning && <span className={'warn-Message'}>{warning}</span>))}
                </div>
                <p className="text-length">{input.value.length ? input.value.length : 0}- {maxLength}</p>
            </React.Fragment>
        }

    </React.Fragment>


)

const dropdownStyles = {
    container: styles => ({
        ...styles,
        borderTopLeftRadius: 0,
        borderBottomLeftRadius: 0,
        position: 'relative',
        flex: '1 1 auto',
        width: '1%',
        marginBottom: 0,
        border: '1px solid #eaeaea',
        padding: '1rem 1.2rem',
        borderRadius: '.5rem',
        backgroundColor: '#fff',
        fontFamily: 'inherit',
        fontSize: '1.4rem',
        '-webkit-appearance': 'none',
        padding: 0
    }),
}

export const renderAsyncCreatableSelect = ({
                                               input,
                                               loadOptions,
                                               label,
                                               defaultOptions,
                                               iconClass,
                                               className,
                                               isMulti,
                                               id,
                                               closeMenuOnSelect=true,
                                               meta: {touched, error, warning}
                                           }) => {
    return (
        <React.Fragment>
            <label className="form__label" htmlFor={input.name}>{label}</label>
            <div className={"input-group " + (error ? "error" : "")}>
                <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className={iconClass}></i>
                    </span>
                </div>
                <AsyncCreatableSelect {...input} className={className}
                                      cacheOptions
                                      id={id}
                                      loadOptions={loadOptions}
                                      defaultOptions={defaultOptions}
                                      isMulti={isMulti}
                                      styles={dropdownStyles}
                                      autoComplete="off"
                                      closeMenuOnSelect={closeMenuOnSelect}
                                      blurInputOnSelect={closeMenuOnSelect}
                                      onBlur={event => event.preventDefault()}
                />
                {   ((<span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))
                }

            </div>
        </React.Fragment>
    )
}
