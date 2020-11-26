import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './needHelp.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectBox } from 'formHandler/formFields';
import NeedHelpForm from 'formHandler/formData/needHelp';
import { createLead } from 'store/SkillPage/NeedHelp/actions';

const NeedHelp = (props) => {

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
    
    const onSubmit = (values) => {
        dispatch(createLead(addHiddenValues(values)));
    }

    return (
        <div className="need-help">
            <h2>Need Help?</h2>
            <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>
                <div className="d-flex">
                    <SelectBox attributes={NeedHelpForm.country_code} register={register} />
                    <InputField attributes={NeedHelpForm.mobile} register={register}
                        errors={!!errors ? errors[NeedHelpForm.mobile.name] : ''} />
                </div>

                <InputField attributes={NeedHelpForm.email} register={register}
                    errors={!!errors ? errors[NeedHelpForm.email.name] : ''} />

                <InputField attributes={NeedHelpForm.name} register={register}
                    errors={!!errors ? errors[NeedHelpForm.name.name] : ''} />

                <button type="submit" className="btn btn-inline btn-primary mx-auto submit-btn" role="button" data-toggle="modal"
                    data-target="#thankyouModal">Submit</button>
            </form>
        </div>
    )
}

export default NeedHelp;