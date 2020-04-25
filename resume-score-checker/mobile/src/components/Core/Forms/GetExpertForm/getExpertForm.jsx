import React , { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import * as Actions from '../../../../stores/scorePage/actions/index';
import './getExpertForm.scss';
import { COUNTRY_CODES } from '../../../../services/countryCode';
import { Toast } from '../../../../services/Toast';

export function Form(hide){
    const { handleSubmit, register, errors, setValue } = useForm()
    const dispatch = useDispatch()
    const onSubmit = async (values, event) => {
        try{
            values.name = values.name.trim()
            let response = await new Promise((resolve, reject) => {
                dispatch(Actions.expertForm({values, resolve, reject}))
            })
            if (response){
                Toast("success", "Form Submitted Successfully");
                event.target.reset();
            }
            else {
                Toast('error', 'Oops! <br> Something went wrong! Try Again');
            }
        }
        catch{
            Toast('error', 'Something went wrong! Try Again');
        }
    }

//Mobile length validation

const [max, setMax] = useState(10)
const [min, setMin] = useState(10)
const maxlen = (event) =>{
    setValue('mobile', '')
    if(!(event.target.value === '+91')){
        setMax(13)
        setMin(0)
    }
    else{
        setMax(10)
        setMin(10)
    }
} 

return (
    <React.Fragment>
    <div className="modal-wrapper" aria-modal aria-hidden tabIndex={-1} role="dialog">
        <div className="modal">
            <div className="getExpertForm">
                <div className="getExpertForm__header">
                    <span onClick={hide} className="sprite back-icon"></span>
                    <strong className="ml-15">Get Help</strong>
                </div>

                <div className="container-box">
                    <p className="getExpertForm__head">Fill the form below to get help</p>
                    <form className="getExpertForm__form" onSubmit = {handleSubmit(onSubmit)}>
                        <ul>
                            <li className={errors.name ? 'form-group error' : 'form-group'}>
                                <div className="floating-label">      
                                    <input className="form--control floating-input" type="text" placeholder=" " name="name" ref={register({
                                        required : true,
                                        pattern : {
                                            value : /^[a-zA-Z\s]+$/
                                        }
                                    })} />
                                    <label>Name</label>
                                </div>
                                {errors?.name?.type === 'required' && <span className="error--mgs">Please Enter Name</span>}
                                {errors?.name?.type === 'pattern' && <span className="error--mgs">Name should not contain special characters</span>}
                            </li>   

                            <li className={errors?.email ? 'form-group error' : 'form-group'}>
                                <div className="floating-label">      
                                    <input className="form--control floating-input" type="email" placeholder=" " name='email' ref={register({
                                        required : true,
                                        pattern: {
                                            value : /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
                                        }
                                    })} />
                                    <label>Email ID</label>
                                </div>
                                {errors?.email?.type === 'required' && <span className="error--mgs">Required</span>}
                                {errors?.email?.type === 'pattern' && <span className="error--mgs">Please enter a valid Email</span>}
                            </li>                 

                            <li className={errors?.mobile ? "getExpertForm__number form-group d-flex error" : "getExpertForm__number form-group d-flex"}>
                                <div className="code">
                                    <select className="form--control floating-select" name = "country_code" ref={register({required: true})} onChange = {maxlen}>
                                        {
                                            COUNTRY_CODES.map((value, index) => {
                                            return <option key= {index} value={value.code}>&nbsp;{value.code}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp; --- &nbsp;&nbsp;&nbsp;{value.country}</option>
                                            })
                                        }
                                    </select>
                                </div>

                                <div className="number"> 
                                    <div className="floating-label">     
                                        <input className="form--control floating-input" type="number" name = 'mobile' placeholder=" " maxLength = {max} ref={register({
                                            required : true,
                                            minLength : min,
                                            pattern : /^[0-9-]+$/
                                        })} />
                                        <label>Number</label>
                                    </div>
                                </div>
                                {errors?.mobile?.type === 'required' && <span className="error--mgs">Required</span>}
                                {errors?.mobile?.type === 'pattern' && <span className="error--mgs">Enter a valid Mobile Number</span>}
                                {errors?.mobile?.type === 'minLength' && <span className="error--mgs">Enter a valid length Number</span>}
                            </li>
                            
                            <li>
                                <button className="btn btn-round-30 btn-blue w-100">Submit</button>
                            </li>
                        </ul>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </React.Fragment>
)}

export default function GetExpertForm({ isFormVisible, hide }){
   return isFormVisible ?  Form(hide) : null
} 