// React Core Import
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { InputField, SelectBox, InputFieldDynamic, TextAreaDynamic } from 'formHandler/desktopFormHandler/formFields';

// Form Import
import { useForm } from 'react-hook-form';

// Inter-App Import
import DetailPageForm from 'formHandler/desktopFormHandler/formData/DetailPage';
import { sendEnquireNow } from 'store/DetailPage/actions';
import {Toast} from '../../../Common/Toast/toast';

// Styling Import
import './enquireNow.scss';
import { imageUrl } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const EnquireNow = (props) => {
    const {location, match: {params: {id}}} = props;
    const sendLearningTracking = useLearningTracking();
    const {product_detail} = useSelector(store => store?.mainCourses);
    const dispatch = useDispatch();
    const { register, handleSubmit, errors } = useForm();

    const addValues = (values) => {
        return {
            ...values,
            'lsource': 2,
            'product': id?.split('-')[1],
            'prd': product_detail?.prd_H1,
            'path': location['pathname']
        }
        // Adding and contributing their values according to contributions
    }

    const onSubmit = async (data, e) => {
        // On submit send data to back-end

        MyGA.SendEvent('SkillNeedHelpForm','ln_need_help', 'ln_need_help_form_submitted', `${data.name}`,'', false, true);

        try {
            await new Promise((resolve) => dispatch(sendEnquireNow({ payload: addValues(data), resolve })));
            e.target.reset(); // reset after form submit
            Toast.fire({ type: 'success', title: 'Your Query Submitted Successfully.' })
        }
        catch (error) {
            Toast.fire({ type: 'error', title: 'Something went wrong!' })
        }

        sendLearningTracking({
            productId: '',
            event: `course_detail_enquire_now_submit_clicked`,
            pageTitle: `course_detail`,
            sectionPlacement: 'enquire_now',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section id="enquire-now" className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="enquire-now mt-30 mb-30">
                        <div className="enquire-now__img col">
                            <img src={`${imageUrl}desktop/enquire-now-bg.png`} alt="Enquire Now" />
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