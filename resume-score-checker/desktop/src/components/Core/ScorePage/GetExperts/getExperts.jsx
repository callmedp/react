import React from 'react';
import './getExperts.scss';
import { useForm } from 'react-hook-form'
import { useDispatch } from 'react-redux';
import * as Actions from '../../../../store/LandingPage/actions/index';
import { Toast } from '../../../../services/Toast';
import  {COUNTRY_CODES} from '../../../../services/countryCodes';
import { siteDomain } from '../../../../utils/domains';
const GetExperts=props=>{

  const { register, handleSubmit, errors, getValues } = useForm()
  const dispatch = useDispatch()
  const onSubmit =async (data,event) =>{
    try{
      await new Promise((resolve, reject) => {
        dispatch(Actions.expertFormSubmit({data, resolve, reject}));
        })
        event.target.reset();
        Toast.fire({
          icon: 'success',
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
        <p>Make your resume more compelling with the help of our professional resume writers, who has helped over 10,000 professional to get interviewed in many companies and get hired quickly. Our experts will not only help in improving your score but also help you in customizing your resume as per your desired job and industry.</p>
        <ul className="expert-help__list mt-5">
          <li className="expert-help__item"><a href={`${siteDomain}/services/resume-writing/63/`}>Resume Writing</a></li>
          <li className="expert-help__item"><a href={`${siteDomain}/services/resume-services/entry-level-freshers/pd-2052`}>Visual Resume</a></li>
          <li className="expert-help__item"><a href={`${siteDomain}/resume-builder/`}>Resume Builder</a></li>
          <li className="expert-help__item"><a href={`${siteDomain}services/resume-services/entry-level-freshers-4/pd-2553/`}>International Resume</a></li>
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
              <input type="text" className="form-control input_field" id="name" name="name" placeholder="Name" ref={register({required : true, pattern : /^[A-Za-z][A-Za-z0-9\s]*$/})} />
              <label htmlFor="name" className="input_label">Name</label>
              {errors?.name?.type === "required" && <span className="error__msg">This field is required</span>}
              {errors?.name?.type === "pattern" && <span className="error__msg">Invalid name</span>}
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
                <input type="text" className="form-control input_field error"  id="number" name="number" placeholder="Mobile" ref={register({required : true,pattern:/^[0-9-]+$/, maxLength:13, validate :{ mobLength : value => getValues('country')!='+91' || value?.length === 10 }})} />
                <label htmlFor="mobile" className="input_label">Mobile</label>
                {errors?.number?.type === "required" && <span className="error__msg">This field is required</span>}
                {errors?.number?.type === "pattern" && <span className="error__msg">Mobile number is not valid!</span>}
                {errors?.number?.type === "maxLength" && <span className="error__msg">Mobile number is not valid!</span>}
                {errors?.number?.type === "mobLength" && <span className="error__msg">Mobile number is not valid!</span>}
              </div>
              </div>
              <button type="submit" className="btn btn-primary btn-round-40 px-5 py-3 mt-3">Submit</button>
            </form>
          </div>
        </div>
  </section>
    );
}

export default  GetExperts;









