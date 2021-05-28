import React from 'react';
import './leadCampaignPage.scss';
import Header from '../../Common/CampaignHeader/campaignHeader';
import Footer from '../../Common/Footer/Footer';
import { useDispatch } from 'react-redux';
import { InputField, SelectBox, SelectBoxCampaign } from 'formHandler/mobileFormHandler/formFields';
import { showSwal } from 'utils/swal';
import { useForm } from 'react-hook-form';
import EnquireNowForm from 'formHandler/mobileFormHandler/formData/enquireNow';
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { fetchLeadManagement } from 'store/LeadManagement/actions';
import { MyGA } from 'utils/ga.tracking.js';
import { Helmet } from 'react-helmet';
import queryString from 'query-string';

const LeadCampaignPage = (props) => {
    const dispatch = useDispatch();
    const { register, handleSubmit, errors } = useForm();
    const { history, location: { search } } = props;
    const campaignQuery = queryString.parse(search);
    
    if(Object.keys(campaignQuery).length === 0) history.push('/404')

    const onSubmit = async (data, e) => {
        data['lsource'] = 162;
        data["source"] = campaignQuery['utm_medium'];
        data["campaign"] = campaignQuery['utm_campaign'] || 'awscloud';
        
        data['extra'] = [];
        data['extra'].push(campaignQuery);

        try {
            await new Promise((resolve, reject) => dispatch(fetchLeadManagement({ payload: data, resolve, reject })));
            e.target.reset(); // reset after form submit
            showSwal('success', 'Thank you for your response');
            history.push('');
        }
        catch (error) {
            showSwal('error', 'Something went wrong!')
        }
    }

    return (
        <div>
            <Helmet>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <Header />
            <section className="m-container mb-50">
                    <div className="m-ja-langingpage mx-auto">
                        <div className="m-ja-form">
                            <div className="m-ja-form__img">
                                <h1 className="m-heading1 ml-30 mt-70">100% guaranteed Job Assistance Programs</h1>
                                <ul>
                                    <li>Google/Azure Certification </li>
                                    <li>Datascience </li>
                                    <li>Six Sigma</li>
                                    <li>Project Management</li>
                                    <li>Digital Marketing</li>
                                    <li>Amazon Web Services ( AWS Certification)</li>
                                </ul>
                            </div>
                            <div className="m-ja-form__form">
                                <form className="mt-30" onSubmit={handleSubmit(onSubmit)}>
                                    <InputField attributes={EnquireNowForm.name} register={register} errors={!!errors ? errors[EnquireNowForm.name.name] : false} />

                                    <InputField attributes={inboxForm.emailCampaign} register={register} errors={!!errors ? errors[inboxForm.emailCampaign.name] : ''} />

                                    <div className="d-flex">
                                            <SelectBox attributes={EnquireNowForm.country_code} register={register} />
                                            <InputField attributes={inboxForm.mobile} register={register} errors={!!errors ? errors[inboxForm.mobile.name] : ''} />
                                    </div>

                                    {/* <div className="custom-select-box w-100"> */}
                                        <SelectBoxCampaign attributes={inboxForm.campaign_code} register={register} />
                                    {/* </div> */}
                                    <button type="submit" className="btn btn-primary submit-btn w-100" role="button">Submit</button>
                                </form>
                                <div className="m-social-links-lp mx-auto mt-50">
                                    <p>Follow us on :</p>
                                    <a href="https://www.facebook.com/shinelearningdotcom/" onClick={() => MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_facebook', 'homepage','', false, true)}>
                                        <figure className="micon-facebook"></figure>
                                    </a>
                                    <a href="https://in.linkedin.com/company/shinelearning" onClick={() => MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_linkedin', 'homepage','', false, true)}>
                                        <figure className="micon-linkedin"></figure>
                                    </a>
                                    <a href="https://twitter.com/shinelearning" onClick={() =>  MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_twitter', 'homepage','', false, true)}>
                                        <figure className="micon-twitter"></figure>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
            </section>
            <Footer />
        </div>
    )
};

export default LeadCampaignPage;