import React from 'react';

const InputField = (props) => {
    const { attributes: {
                            className, type, 
                            name, value, 
                            validation, 
                            label,defaultValue,
                            errorMessage, id, placeholder
                        }, 
            errors,
            register } = props
    
    return (
        <div className={ !!errors ? "form-group error" : "form-group"}>
            <input className={className} type={type} name={name}
                placeholder={placeholder} ref={register(validation)} value={value}
                defaultValue={defaultValue} id={id} />
            <label htmlFor={name}>{label}</label>
            { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''}
        </div>
    )
}

const SelectBox = (props) => {

    const { attributes: {
                            name, children, validation
                        }, register } = props

    return (
        <div className="custom-select-box">
            <select name={name} className="custom-select" ref={register(validation)} aria-label="select country name">
                { children?.map((item,index)=>{
                    return(
                    <option value={item.value} key={index}>{item.value}&nbsp;&nbsp; -- &emsp;{item.text}</option>
                    )
                })}
            </select>
        </div>
    )
}

const TextArea = (props) => {
    const { attributes: { className, label, type, name, value, validation, defaultValue, id, errorMessage, rows, placeholder }, errors, register } = props;

    return (

        
        <React.Fragment>
            <div className={`add-comments ${!!errors ? "form-group error" : "form-group"}`}>
                <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} rows={rows} id={id} />
                <label htmlFor={name}>{label}</label>
                { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''}
            </div>
        </React.Fragment>
    )
}


const InputFieldDynamic = (props) => {
    const { attributes: {
                            className, type, 
                            name, value, form_class_name, 
                            validation, 
                            label,defaultValue,
                            errorMessage, id, placeholder
                        }, 
            errors,
            register } = props
    
    return (
        <div className={ !!errors ? `${form_class_name} error` : `${form_class_name}`}>
            <input className={className} type={type} name={name}
                placeholder={placeholder} ref={register(validation)} value={value}
                defaultValue={defaultValue} aria-required="true" aria-invalid="true" id={id} />
            <label>{label}</label>
            { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''}
        </div>
    )
}


const TextAreaDynamic = (props) => {
    const { attributes: { className, label, type, name, value, form_class_name, validation, defaultValue, id, rows, placeholder }, errors, register } = props;

    return (

        
        <React.Fragment>
            <div className={ !!errors ? `${form_class_name} error` : `${form_class_name}`}>
                <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} rows={rows} id={id} />
                <label htmlFor={name}>{label}</label>
            </div>
        </React.Fragment>
    )
}

export {
    InputField,
    SelectBox,
    TextArea,
    InputFieldDynamic,
    TextAreaDynamic
}