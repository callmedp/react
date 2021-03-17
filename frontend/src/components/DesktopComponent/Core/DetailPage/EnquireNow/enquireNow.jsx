// React Core Import
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { InputField, SelectBox, InputFieldDynamic, TextAreaDynamic } from 'formHandler/desktopFormHandler/formFields';

// Form Import
import { useForm } from 'react-hook-form';

// Inter-App Import
import DetailPageForm from 'formHandler/desktopFormHandler/formData/DetailPage';

// Styling Import
import './enquireNow.scss';

const EnquireNow = (props) => {
    const { history } = props;
    const { register, handleSubmit, errors } = useForm();


    console.log(errors)

    const addValues = (values) => {
        // Adding and contributing their values according to contributions
    }

    const onSubmit = async (data) => {
        // On submit send data to back-end

    }

    return (
        <section id="enquire-now" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="enquire-now mt-30 mb-30">
                        <div className="enquire-now__img col">
                            <img src="/media/images/desktop/enquire-now-bg.png" alt="Enquire Now" />
                        </div>
                        <div className="enquire-now__form col">
                            <strong className="heading2">Enquire now!</strong>
                            <form className="mt-30" onSubmit={handleSubmit(onSubmit)}>

                                <InputField attributes={DetailPageForm.name} register={register}
                                    errors={!!errors ? errors[DetailPageForm.name.name] : false} />

                                <div className="d-flex">

                                    <SelectBox attributes={DetailPageForm.country_code} register={register} />

                                    <InputFieldDynamic attributes={DetailPageForm.mobile} register={register}
                                        errors={!!errors ? errors[DetailPageForm.mobile.name] : false} />

                                </div>

                                <TextAreaDynamic attributes={DetailPageForm.message} register={register}
                                    errors={!!errors ? errors[DetailPageForm.message.name] : false} />

                                <button type="submit" className="btn btn-inline btn-primary submit-btn" role="button">Submit</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default EnquireNow;