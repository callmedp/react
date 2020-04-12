import React from 'react';
import './getExperts.scss';
import { useForm } from 'react-hook-form'
import { useDispatch } from 'react-redux';
import * as Actions from '../../../../store/LandingPage/actions/index';
import { Toast } from '../../../../services/Toast';
import  {COUNTRY_CODES} from '../../../../services/countryCodes';

const GetExperts=props=>{

  const { register, handleSubmit, errors } = useForm()
  const dispatch = useDispatch()
  const onSubmit =async (data,event) =>{
    try{
      await new Promise((resolve, reject) => {
        dispatch(Actions.expertFormSubmit({data, resolve, reject}));
        })
        event.target.reset();
        Toast.fire({
          icon: 'sucess',
          html : '<h3>Submitted Successfully!<h3>'
        })
        
    }catch(e){
      Toast.fire({
        icon: 'error',
        html : '<h3>Something went wrong! Try again.<h3>'
      })
    }
  } 
    return (

<section className="container expert-help" id="getexpert">
    <div className="row">
      <div className="col-md-8 pr-5">
        <h2><span>Get Expert Help</span></h2>
        <p>Shine Learning is India’s largest professional courses and career skills portal. Launched by Shine.com, Shine Learning has a vision to up-skill the Indian talent pool to adapt to the changing job market.Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
        <ul className="expert-help__list mt-5">
          <li className="expert-help__item">Resume Writing</li>
          <li className="expert-help__item">Resume Writing</li>
          <li className="expert-help__item">Resume Writing</li>
          <li className="expert-help__item">Resume Writing</li>
        </ul>
      </div>

        <div className="col-md-4 expert-help__login need-help pl-5">
          <h3>Fill the form below to get help</h3>

          <form className="mt-5" id="callUsForm" onSubmit={handleSubmit(onSubmit)}  noValidate="novalidate">

            <div className={errors?.email ? "form-group error" : "form-group"} >
              <input type="text" className="form-control input_field" id="email" name="email" placeholder="Email" ref={register({required:true,pattern:/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/})} />
              <label htmlFor="email" className="input_label" >Email</label>
              {errors?.email?.type === "required" && <span className="error__msg">This field is required</span>}
              {errors?.email?.type === "pattern" && <span className="error__msg">Email address is invalid!</span>}
            </div>
  
            <div className={errors?.name ? "form-group error" : "form-group"}>
              <input type="text" className="form-control input_field" id="name" name="name" placeholder="Name" ref={register({required : true,pattern:/^[A-Za-z_]+[0-9]+(\s)*([A-Za-z_]+[0-9]+)*$/})} />
              <label htmlFor="name" className="input_label">Name</label>
              {errors?.name?.type === "required" && <span className="error__msg">This field is required</span>}
              {errors?.name?.type === "pattern" && <span className="error__msg">Name should not start with digits!</span>}
            </div>
            <div className="d-flex expert-help__mobile">
              <div className="custom-select-box">
                    <select name="country" className="custom-select" id="country-code" ref={register({required:true})}>
                      { 
                      COUNTRY_CODES.map((item,index)=>{
                      return (
                        <option value={item.code} key={index}>
                        {item.code}&nbsp;&nbsp;&nbsp;&nbsp; -- &nbsp;&nbsp;&nbsp;&nbsp;{item.country}
                        </option>
                      )
                      })
                    }
                </select>
              </div>
              
              <div className={ errors.number ? "form-group expert-help__mobile--mobile error " : "form-group expert-help__mobile--mobile"}>
                <input type="text" className="form-control input_field error"  id="number" name="number" placeholder="Mobile" ref={register({required : true,pattern:/^[0-9-]+$/})} />
                <label htmlFor="mobile" className="input_label">Mobile</label>
                {errors?.number?.type === "required" && <span className="error__msg">This field is required</span>}
                {errors?.number?.type === "pattern" && <span className="error__msg">Mobile number is not valid!</span>}
              </div>
            </div>
            <button type="submit" className="btn btn-primary btn-round-40 px-5 py-3 mt-3">Submit</button></form>
        </div>

    </div>
  </section>
    );
}

export default  GetExperts;









