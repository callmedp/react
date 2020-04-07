import React from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import * as Actions from '../../../../stores/scorePage/actions/index';
import './getExpertForm.scss';
import Swal from 'sweetalert2';

export function Form(hide){
    const { handleSubmit, register, errors } = useForm()
    const dispatch = useDispatch()
    const onSubmit = async (values, event) => {
        let response = await new Promise((resolve, reject) => {
            dispatch(Actions.expertForm({values, resolve, reject}))
        })
        if (response){
            Swal.fire({
                icon : 'success',
                title : 'Form Submitted Successfully !'
            })
            event.target.reset();
        }
        else {
            Swal.fire({
                icon : 'error',
                title : 'Something went wrong! Try again'
            })
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
                                            value : /^\w+/
                                        }
                                    })} />
                                    <label>Name</label>
                                </div>
                                {errors.name && <span className="error--mgs">Please Enter Name</span>}
                            </li>   

                            <li className={errors?.email ? 'form-group error' : 'form-group'}>
                                <div className="floating-label">      
                                    <input className="form--control floating-input" type="text" placeholder=" " name='email' ref={register({
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
                                    <select className="form--control floating-select" name = "country_code" ref={register({required: true})}>
                                        <option value="+91">+91</option>
                                        <option value="+92">+92</option>
                                        <option value="+2345">+2345</option>
                                        <option value="+9834">+9834</option>
                                    </select>
                                </div>

                                <div className="number"> 
                                    <div className="floating-label">      
                                        <input className="form--control floating-input" type="text" name = 'mobile' placeholder=" " ref={register({
                                            required : true,
                                            pattern : /^[0-9-]+$/
                                        })} />
                                        <label>Number</label>
                                    </div>
                                </div>
                                {errors?.mobile?.type === 'required' && <span className="error--mgs">Required</span>}
                                {errors?.mobile?.type === 'pattern' && <span className="error--mgs">Enter a valid Mobile Number</span>}
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