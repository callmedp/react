import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Multiselect from 'react-widgets/lib/Multiselect'
import moment from 'moment'
import addDays from "date-fns/addDays";
import AsyncCreatableSelect from 'react-select/async-creatable';


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                iconClass,
                                id,
                                prepend,
                                meta: {touched, error, warning}
                            }) => (

        
        <React.Fragment>
            <label className="form__label" htmlFor={input.name}>{label}</label>
            {!prepend ?
                <React.Fragment>
                    <input {...input} className={className +(touched && error ? " error" : "")} id={id} type={type} autoComplete="off"/>
                    {touched &&
                        ((<span className={'error-message'}>{error}</span>) ||
                            (warning && <span className={'warn-Message'}>{warning}</span>))
                    }
                </React.Fragment> :
                
            <div className={"input-group " + (touched && error ? "error" : "")} >
                <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
                </div>
                <input {...input} className={className} id={id} type={type} autoComplete="off"/>
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
        <input {...input} className={className} onClick={(e) => tillTodayDisable(index, !input.checked, e)} id={id} type={type}/>
    </React.Fragment>
);

const Input = ({onChange, placeholder, value, isSecure, id, onClick,name,disabled}) => (
    <input
        onChange={onChange}
        placeholder={placeholder}
        value={value}
        isSecure={isSecure}
        name={name}
        id={id}
        onClick={onClick}
        disabled={disabled}
        autoComplete="off"
        readonly="true"
    />
);

export const datepicker =
    ({
         input,
         label,
         className,
         id,
         disabled,
         minDate,
         yearDropDownItemNumber,
         meta: {touched, error, warning}
     }) => (
        <React.Fragment>
            <label className="form__label" htmlFor={input.name}>{label}</label>
            <div className={"input-group " + (touched && error ? "error" : "")}>
                <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className="sprite icon--date"></i>
                    </span>
                </div>
                <DatePicker customInput={<Input id={id} name={input.name} disabled={disabled} />}
                            value={disabled ? moment().format('YYYY-MM-DD').toString() : input.value}
                            className={className}
                            dateFormat="yyyy-MM-dd"
                            autoComplete="off"
                            selected={input.value ? new Date(input.value) : null}
                            maxDate={new Date()}
                            id={id}
                            onChange={date => input.onChange(date)}
                            showYearDropdown
                            yearDropdownItemNumber={yearDropDownItemNumber}
                            scrollableYearDropdown
                            showMonthDropdown
                            disabledKeyboardNavigation={true}
                            disabled={disabled}
                            disabledNavigation
                            withPortal
                            minDate={minDate ? addDays(new Date(minDate),1) : null}
                />
                {touched &&  ((error && <span className={'error-message'}>{error}</span>) ||
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
        <div className={"input-group " +(touched && error ? "error" : "")}>
            <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
            </div>
            <select {...input} className={className}
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



            <select {...input} className={className +(touched && error ? " error" : "")}
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


export const renderMultiselect = ({ input,className, data, valueField, textField,defaultValue }) =>(
    
    <React.Fragment>
        <label className="form__label" htmlFor="extracurricular">Interest</label>
        <div className="input-group">

            <Multiselect {...input}
                onBlur={() => input.onBlur()}
                value={input.value.length ? input.value :defaultValue}
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
                                   className,
                                   iconClass,
                                   prepend,
                                   meta: {touched, error, warning}

                               }) => (
    <React.Fragment>
        <label className="form__label" htmlFor={input.name}>{label}</label>
        {prepend ?
        <div className="input-group">
            <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
            </div>
            <textarea {...input} placeholder={label} type={type} className={className} rows={rows}/>
            <div>
                {touched &&
                ((error && <span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))}
            </div>
        </div>:
        <React.Fragment>
            <textarea {...input} placeholder={label} type={type} className={className} rows={rows}/>
            <div>
                {touched &&
                ((error && <span className={'error-message'}>{error}</span>) ||
                    (warning && <span className={'warn-Message'}>{warning}</span>))}
            </div>
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
                         padding:0 }),
}

export const renderAsyncCreatableSelect = ({
    input,
    loadOptions,
    label,
    defaultOptions,
    iconClass,
    className,
    isMulti,
    closeMenuOnSelect,
    meta: {touched, error, warning}
}) => {
        return (
            <React.Fragment>
                <label className="form__label" htmlFor={input.name}>{label}</label>
                <div className={"input-group " + (touched && error ? "error" : "")} >
                    <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className={iconClass}></i>
                    </span>
                    </div>
                    <AsyncCreatableSelect {...input} className={className}
                                cacheOptions
                                loadOptions={loadOptions}
                                // styles={{menuPortal: base => ({...base, zIndex: 9999})}}
                                // menuPortalTarget={document.getElementById('right-panel-section')}
                                // menuPosition={'absolute'}
                                // menuPlacement={'auto'}
                                // value={'New Value'}
                                defaultOptions={[{value:'Enter atleast 3 characters to search',label:'Enter atleast 3 characters to search'}]}
                                // placeholder={input.value}
                                // value={input.value}
                                // isMulti={isMulti}
                                styles={dropdownStyles}
                                autoComplete="off"
                                // closeMenuOnSelect={closeMenuOnSelect}
                                onBlur={event => event.preventDefault()}
                        />
                    {touched &&
                        ((<span className={'error-message'}>{error}</span>) ||
                            (warning && <span className={'warn-Message'}>{warning}</span>))
                    }
                
                </div>
            </React.Fragment>
        )
}
