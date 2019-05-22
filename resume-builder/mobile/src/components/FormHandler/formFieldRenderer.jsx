import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Multiselect from 'react-widgets/lib/Multiselect'


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


export const datepicker =
    ({
         input,
         label,
         className,
         id,
         disabled,
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
                <DatePicker {...input} dateFormat="yyyy-MM-dd" className={className}
                        value={disabled ? "This is disabled" : input.value}
                        selected={input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)} id={id} disabled={disabled} autoComplete="off"
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
                    ////console.log(input.label)
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
                    ////console.log(input.label)
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

