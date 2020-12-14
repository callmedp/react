import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';
import './modals.scss'
import { useForm } from 'react-hook-form';
import { InputField, SelectBox } from 'formHandler/mobileFormHandler/formFields'
import EnquireNowForm from 'formHandler/mobileFormHandler/formData/enquireNow';
import { createLead } from 'store/SkillPage/NeedHelp/actions';

const EnquiryModal = (props) => {
    const { setEnquiryForm } = props
    const { register, handleSubmit, errors } = useForm()
    const { id, heading, absolute_url } = useSelector( store => store.skillBanner )
    const dispatch = useDispatch()

    const addHiddenValues = (values) =>{
        return {
            ...values,
            'lsource': 1,
            'product': id,
            'prd': heading,
            'path': absolute_url
        }
    }

    const onSubmit = async (values, event) => {
        const data = addHiddenValues(values)
        const result = await new Promise((resolve) => dispatch(createLead({data, resolve})));
        if(result){
            event.target.reset();
            setEnquiryForm(false);
        }
    }

    return(
        <div className="m-container m-enquire-now m-form-pos-btm pb-10">
            <span className="m-close" onClick={()=>setEnquiryForm(false)}>x</span>
            <h2 className="m-heading2 text-center">Enquire now!</h2>
            <p className="text-center">Share your query, our experts will help you take  your career forward!</p>
            <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>
                <InputField attributes={EnquireNowForm.name} register={register}
                    errors={!!errors ? errors[EnquireNowForm.name.name] : ''} />
                <InputField attributes={EnquireNowForm.email} register={register}
                    errors={!!errors ? errors[EnquireNowForm.email.name] : ''} />
                <div className="d-flex">
                    <SelectBox attributes={EnquireNowForm.country_code} register={register} />
                    <InputField attributes={EnquireNowForm.mobile} register={register}
                        errors={!!errors ? errors[EnquireNowForm.mobile.name] : ''} />
                </div>
                <div className="m-form-group">
                    <button className="btn-blue">Submit</button>
                </div>

            </form>
        </div>
    )
}

export default EnquiryModal;