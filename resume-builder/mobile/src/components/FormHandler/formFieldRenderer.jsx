import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AsyncSelect from 'react-select/lib/Async';


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
                    <input {...input} className={className +(error ? " error" : "")} id={id} type={type}/>
                    {touched &&
                        ((<span className={'error-message'}>{error}</span>) ||
                            (warning && <span className={'warn-Message'}>{warning}</span>))
                    }
                </React.Fragment> :
                
            <div className={"input-group " + (error ? "error" : "")} >
                <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
                </div>
                <input {...input} className={className} id={id} type={type}/>
                {touched &&
                    ((<span className={'error-message'}>{error}</span>) ||
                        (warning && <span className={'warn-Message'}>{warning}</span>))
                }
            
            </div>
            }
        </React.Fragment>
);


export const datepicker =
    ({
         input,
         label,
         className,
         id,
         meta: {touched, error, warning}
     }) => (
        <React.Fragment>
            <label className="form__label" htmlFor={input.name}>{label}</label>
            <div className={"input-group " + (error ? "error" : "")}>
                <div className="input-group__prepend">
                    <span className="input-group__text">
                        <i className="sprite icon--date"></i>
                    </span>
                </div>
                <DatePicker {...input} dateFormat="yyyy-MM-dd" className={className}
                        selected={input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)} id={id}
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
        <div className={"input-group " +(error ? "error" : "")}>
            <div className="input-group__prepend">
                <span className="input-group__text">
                    <i className={iconClass}></i>
                </span>
            </div>
            <select {...input} className={className}
                onBlur={() => {
                    input.onBlur(input.value)
                    console.log(input.label)
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



            <select {...input} className={className +(error ? " error" : "")}
                onBlur={() => {
                    input.onBlur(input.value)
                    console.log(input.label)
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


export const renderDynamicSelect = ({
                                        input,
                                        loadOptions,
                                        label,
                                        defaultOptions,
                                        meta: {touched, error, warning}
                                    }) => (
    <div className="flex-auto">
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
        ((error && <span className={'error-message'}>{error}</span>) ||
            (warning && <span className={'warn-Message'}>{warning}</span>))}
    </div>
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

