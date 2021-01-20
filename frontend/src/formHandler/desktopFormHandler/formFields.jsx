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
        <div className={ !!errors ? "form-group error" : "form-group"}>
            <input className={className} type={type} name={name}
                id={id} placeholder=" " ref={register(validation)} value={value}
                defaultValue={defaultValue} />
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
    const { attributes: { className, type, name, value, validation, defaultValue, id, rows }, register } = props;

    return (
        <React.Fragment>
            <textarea className={className} type={type} name={name} id={id} placeholder=" " ref={register(validation)} value={value} defaultValue={defaultValue} rows={rows} />
            {/* { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''} */}
        </React.Fragment>
    )
}

export {
    InputField,
    SelectBox,
    TextArea
}