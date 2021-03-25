import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';
import './modals.scss'
import { useForm } from 'react-hook-form';
import { InputField, SelectBox } from 'formHandler/mobileFormHandler/formFields'
import EnquireNowForm from 'formHandler/mobileFormHandler/formData/enquireNow';
import { createLead } from 'store/SkillPage/NeedHelp/actions';
import { startNeedHelpLoader, stopNeedHelpLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';

const EnquiryModal = (props) => {
    const { setEnquiryForm, page } = props
    const { register, handleSubmit, errors } = useForm()
    const { id, heading, absolute_url } = useSelector( store => store.skillBanner )
    const { needHelpLoader } = useSelector(store => store.loader);
    const { product_detail } = useSelector( store => store.mainCourses )
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

    const addProductValues = (values) => {
        return {
            ...values,
            'lsource': 2,
            'product': product_detail?.prd_product,
            'prd': product_detail?.prd_H1,
            'path': absolute_url
        }
    }

    const onSubmit = async (values, event) => {
        const data = page === 'detailPage' ?  addProductValues(values) : addHiddenValues(values)
        try{
            dispatch(startNeedHelpLoader())
            const result = await new Promise((resolve) => dispatch(createLead({data, resolve})));
            dispatch(stopNeedHelpLoader())
            if(result){
                event.target.reset();
                setEnquiryForm(false);
            }
        }
        catch(e){
            dispatch(stopNeedHelpLoader())
            console.log(e)
        }
        
    }

    return(
        <>
            {
                needHelpLoader && <Loader />
            }
            <div className="m-container m-enquire-now m-form-pos-btm pb-10" data-aos="fade-up" data-aos-duration="500">
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
        </>
    )
}

export default EnquiryModal;