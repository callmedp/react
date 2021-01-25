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
    // console.log(props);
    const { attributes: { className, type, name, value, validation, defaultValue, id, rows, placeholder }, register } = props;

    return (
        <React.Fragment>
            <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} rows={rows} />
            {/* <label htmlFor={name}>{label}</label> */}
            {/* { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''} */}
        </React.Fragment>
    )
}

export {
    InputField,
    SelectBox,
    TextArea
}