import React from 'react';
import { useDispatch, useSelector, connect } from 'react-redux';
import './needHelp.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectBox } from 'formHandler/desktopFormHandler/formFields';
import NeedHelpForm from 'formHandler/desktopFormHandler/formData/needHelp';
import { createLead } from 'store/SkillPage/NeedHelp/actions';
import { MyGA } from 'utils/ga.tracking.js';

const NeedHelp = (props) => {

    const { register, handleSubmit, errors } = useForm()
    const { id, heading, absolute_url } = useSelector( store => store.skillBanner )
    const { gaTrack } = props;
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
        }
    }

    return (
        <div className="need-help" id="help">
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
                    data-target="#thankyouModal" onClick={() => gaTrack('SkillNeedHelpForm','ln_need_help', 'ln_need_help_form_submitted', heading,'', false, true)}>Submit</button>
            </form>
        </div>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "gaTrack": (data) => {
             MyGA.SendEvent(data)
        }
    }
}

export default connect(null, mapDispatchToProps)(NeedHelp);