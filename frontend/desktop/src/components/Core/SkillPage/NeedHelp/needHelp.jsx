import React from 'react';
import { useDispatch } from 'react-redux';
import './needHelp.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectBox } from 'formHandler/formFields';
import NeedHelpForm from 'formHandler/formData/needHelp';
import { createLead } from 'store/SkillPage/NeedHelp/actions/index';

const NeedHelp = (props) => {

    const { register, handleSubmit, errors } = useForm()
    const dispatch = useDispatch()

    const onSubmit = (value) => {
        dispatch(createLead(value));
    }

    return (
        <div className="need-help">
            <h2>Need Help?</h2>
            <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>
                <div className="d-flex">
                    {/* <div className="custom-select-box">
                        <select className="select" className="custom-select">
                            <option selected>+91</option>
                            <option value="+91">+91</option>
                            <option value="+92">+92</option>
                            <option value="+93">+93</option>
                        </select>
                    </div> */}
                    {/* <div className="form-group">
                            <input type="text" className="form-control" id="mobile" name="mobile"
                                placeholder=" " value="" aria-required="true" aria-invalid="true" />
                            <label for="">Mobile</label>
                        </div> */}
                    <SelectBox attributes={NeedHelpForm.country_code} register={register} />
                    <InputField attributes={NeedHelpForm.mobile} register={register}
                        errors={!!errors ? errors[NeedHelpForm.mobile.name] : ''} />
                </div>
                {/* <div className="form-group error">
                        <input type="email" className="form-control" id="email" name="email" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Email</label>
                        <span className="error-msg">Required</span>
                    </div> */}

                <InputField attributes={NeedHelpForm.email} register={register}
                    errors={!!errors ? errors[NeedHelpForm.email.name] : ''} />

                {/* <div className="form-group">
                        <input type="text" className="form-control" id="name" name="name" placeholder=" "
                            value="" aria-required="true" aria-invalid="true" />
                        <label for="">Name</label>
                    </div> */}
                <InputField attributes={NeedHelpForm.name} register={register}
                    errors={!!errors ? errors[NeedHelpForm.name.name] : ''} />

                <button type="submit" className="btn btn-inline btn-primary mx-auto submit-btn" role="button" data-toggle="modal"
                    data-target="#thankyouModal">Submit</button>
            </form>
        </div>
    )
}

export default NeedHelp;