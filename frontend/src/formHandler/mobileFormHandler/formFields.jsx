import React, { useState } from 'react';

const InputField = (props) => {
    const { attributes: {
                            className, type, 
                            name, value, 
                            validation, 
                            label,defaultValue,
                            errorMessage, id, 
                            placeholder
                        }, 
            errors,
            register,
            customClass } = props
    
    return (
        <div className={ customClass ? customClass : !!errors ? "m-form-group m-error flex-1" : "m-form-group flex-1" }>
            <input className={className} type={type} name={name} 
            id={id} placeholder={placeholder ? placeholder : ' '} ref={register(validation)} value={value}
            defaultValue={defaultValue}/>
            <label className="input-label" htmlFor={name}>{label}</label>
            { !!errors ? <span className="error_cls">{errorMessage[errors.type]}</span> : ''}
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
    const { attributes: { className, type, name, value, validation, defaultValue, rows, placeholder, label, errorMessage }, register, errors } = props;

    return (
        <>  
            <div className="m-form-group">
                <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} id={name} rows={rows} />
                <label className="input-label" htmlFor={name}>{label}</label>
                { !!errors ? <span className="error_cls">{errorMessage[errors.type]}</span> : ''}
            </div>
        </>
    )
}


const SelectExperienceBox = (props) => {

    const { attributes: {
                            name, children, validation
                        }, register } = props

    const [checkedClass, setCheckedClass] = useState('form-group')

    return (
        <div className={checkedClass}>
            <div className="custom-select-box">
                <select name={name} className="custom-select" ref={register(validation)} aria-label="select experience level" onChange={() => setCheckedClass('form-group checked')}>
                    { children?.map((item,index)=>{
                        return(
                        <option value={item.value} key={index}>{item.text}</option>
                        )
                    })}
                </select>
            </div>
        </div>
    )
}

const MultiSelectBox = (props) => {
    const [mouse, setMouse] = useState(false);
    const { attributes: {
        className, type, 
        name, value, 
        validation, 
        label,defaultValue,
        errorMessage, id, placeholder
    }, register, errors, data } = props

    return (<>
        {
            mouse ?

                <div className="form-group" onClick={() => setMouse(false)}>
                    <label for="">Your skills</label>
                    <input className="form-control" type="text" name={name} ref={register(validation)} />
                </div>

                :

                <div className="form-group-custom pos-rel" >
                    <label className="sticky-label" htmlFor="">Your skills</label>
                    <div className="custom-textarea">
                        {data?.map((data, i) => {
                            return (
                                <label className="label-added" for="">{data}</label>
                            )
                        })
                        }
                        <span className="d-flex align-items-center mt-10">
                            <input type="text" name={name} className="form-control custom-input" ref={register(validation)} defaultValue={defaultValue} id={id} placeholder={placeholder} />
                        </span>
                    </div>
                { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''}
                </div>
        }
    </>)

}

export {
    InputField,
    SelectBox,
    TextArea,
    SelectExperienceBox,
    MultiSelectBox
}