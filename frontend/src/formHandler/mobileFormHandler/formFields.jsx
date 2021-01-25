import React from 'react';

const InputField = (props) => {
    const { attributes: {
                            className, type, 
                            name, value, 
                            validation, 
                            label,defaultValue,
                            errorMessage, id, 
                        }, 
            errors,
            register } = props
    
    return (
        <div className={ !!errors ? "m-form-group m-error flex-1" : "m-form-group flex-1"}>
            <input className={className} type={type} name={name} 
            id={id} placeholder=" " ref={register(validation)} value={value}
            defaultValue={defaultValue}/>
            <label className="m-input_label" htmlFor={name}>{label}</label>
            { !!errors ? <span className="m-error-msg">{errorMessage[errors.type]}</span> : ''}
        </div>
    )
}

const SelectBox = (props) => {

    const { attributes: {
                            name, children, validation
                        }, register } = props

    return (
        <div className="m-custom-select-box">
            <select name={name} className="m-custom-select" ref={register(validation)}>
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
    const { attributes: { className, type, name, value, validation, defaultValue, rows, placeholder, label }, register } = props;

    return (
        <>
            <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} id={name} rows={rows} />
            {/* <label htmlFor={name}>{label}</label> */}
        </>
    )
}

export {
    InputField,
    SelectBox,
    TextArea
}