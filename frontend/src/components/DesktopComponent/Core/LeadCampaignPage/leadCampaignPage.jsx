import React from 'react';
import './leadCampaignPage.scss';
import CampaignHeader from '../../Common/CampaignHeader/campaignHeader';
import { useDispatch } from 'react-redux';
import { InputField, SelectBox, SelectBoxCampaign } from 'formHandler/desktopFormHandler/formFields';
import {Toast} from '../../Common/Toast/toast';
import { useForm } from 'react-hook-form';
import NeedHelpForm from 'formHandler/desktopFormHandler/formData/needHelp';
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
            Toast.fire({ type: 'success', title: 'Thank you for your response' })
            history.push('');
        }
        catch (error) {
            Toast.fire({ type: 'error', title: 'Something went wrong!' })
        }
    }

    return (
        <div>
            <Helmet>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <CampaignHeader />
            <section className="container-fluid">
                <div className="row">
                    <div className="ja-langingpage mx-auto">
                        <div className="ja-form">
                            <div className="ja-form__img">
                                <h1 className="heading1 ml-30 mt-70">100% guaranteed Job Assistance Programs</h1>
                                <ul>
                                    <li>Google/Azure Certification </li>
                                    <li>Datascience </li>
                                    <li>Six Sigma</li>
                                    <li>Project Management</li>
                                    <li>Digital Marketing</li>
                                    <li>Amazon Web Services ( AWS Certification)</li>
                                </ul>
                            </div>
                            <div className="ja-form__form flex-1">
                                <form className="mt-30" onSubmit={handleSubmit(onSubmit)}>
                                    <InputField attributes={NeedHelpForm.name} register={register} errors={!!errors ? errors[NeedHelpForm.name.name] : false} />

                                    <InputField attributes={NeedHelpForm.emailCampaign} register={register} errors={!!errors ? errors[NeedHelpForm.emailCampaign.name] : ''} />

                                    <div className="d-flex">
                                        <SelectBox attributes={NeedHelpForm.country_code} register={register} />
                                        <InputField attributes={NeedHelpForm.mobile} register={register} errors={!!errors ? errors[NeedHelpForm.mobile.name] : ''} />
                                    </div>

                                    <div className="custom-select-box w-100">
                                        <SelectBoxCampaign attributes={NeedHelpForm.campaign_code} register={register} />
                                    </div>
                                    <button type="submit" className="btn btn-primary submit-btn w-100" role="button">Submit</button>
                                </form>
                                <div className="social-links-lp mx-auto mt-50">
                                    <p>Follow us on :</p>
                                    <a href="https://www.facebook.com/shinelearningdotcom/" className="icon-facebook mt-0" onClick={() =>  MyGA.SendEvent('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'facebook','', false, true)}></a>
                                    <a  href="https://in.linkedin.com/company/shinelearning" className="icon-linkedin" onClick={() =>  MyGA.SendEvent('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'linkedin','', false, true)}></a>
                                    <a href="https://twitter.com/shinelearning" className="icon-twitter mt-5" onClick={() =>  MyGA.SendEvent('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'twitter','', false, true)}></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            {/* <Footer /> */}
        </div>
    )
};

export default LeadCampaignPage;