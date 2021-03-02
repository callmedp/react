import React, { useState } from 'react';

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
        <div className={ !!errors ? "form-group error" : "form-group" }>
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
    const { attributes: { className, label, type, name, value, validation, defaultValue, id, rows, placeholder }, register } = props;

    return (

        
        <React.Fragment>
            <div className="form-group add-comments">
                <textarea className={className} name={name} type={type} placeholder={placeholder} ref={register(validation)} value={value} defaultValue={defaultValue} rows={rows} id={id} />
                <label htmlFor={name}>{label}</label>
            </div>
        </React.Fragment>
    )
}

const SelectIntentBox = (props) => {

    const { attributes: {
                            name, children, validation, label ,errorMessage
                        }, register, errors } = props

    const [checkedClass, setCheckedClass] = useState('form-group')

    const handleSelect = (e) => {
        if(e.target.value){
            setCheckedClass('form-group checked')
        }
        else{
            setCheckedClass('form-group')
        }
    }

    return (
        <div className={!!errors ? 'form-group error' : checkedClass}>
            <div className="custom-select-box">
                <select name={name} className="custom-select" ref={register(validation)} aria-label={label} onChange={(e) => handleSelect(e)}>
                    { children?.map((item,index)=>{
                        return(
                        <option value={item.value} key={index}>{item.text}</option>
                        )
                    })}
                </select>
                { !!errors ? <span className="error-msg">{errorMessage[errors.type]}</span> : ''}
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
                    <label htmlFor="">Your skills</label>
                    <input className="form-control" type="text" name={name} ref={register(validation)} autoComplete="off" />
                </div>

                :

                <div className={data?.length ? "form-group-custom checked" : "form-group-custom"}>
                    <label className="sticky-label" htmlFor="">Your skills</label>
                    <div className="custom-textarea">
                        {data?.map((data, i) => {
                            return (
                                <label className="label-added" htmlFor="">{data}</label>
                            )
                        })
                        }
                        <span className="d-flex align-items-center mt-10">
                            <input type="text" className="form-control custom-input" name={name} ref={register(validation)} defaultValue={defaultValue} id={id} placeholder={placeholder} autoComplete="off" />
                            <button className="custom-btn" type="submit"><figure className="icon-search-arrow"></figure></button>
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
    SelectIntentBox,
    MultiSelectBox
}