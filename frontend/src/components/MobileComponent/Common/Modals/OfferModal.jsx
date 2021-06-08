import React from 'react';
import './modals.scss';
import { useDispatch } from 'react-redux';
import { useForm } from 'react-hook-form';
import OfferTimer from 'utils/OfferTimer';
import { InputField, SelectBox } from 'formHandler/mobileFormHandler/formFields';
import EnquireNowForm from 'formHandler/mobileFormHandler/formData/enquireNow';
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { fetchLeadManagement } from 'store/LeadManagement/actions';
// import '../../Core/HomePage/OfferEnds/offerEnds.scss';

const OfferModal = (props) => {
    const {showOffer, handleOfferClose, navOffer, setOfferStatus} = props;
    const dispatch = useDispatch();
    const { register, handleSubmit, errors } = useForm();

    const onSubmit = async (values, event) => {
        values['course'] = navOffer[2];
        values['product_offer'] = true;
        values['msg'] = `${navOffer[1]} - ${navOffer[3]}`;
        values['lsource'] = 34;
        values["source"] = navOffer[2];
        values["campaign"] = 'homepage-banner';

        const result = await new Promise((resolve, reject) => dispatch(fetchLeadManagement({ payload: values, resolve, reject })))
        if(result.status) {
            handleOfferClose(false);
            setOfferStatus(true);
        }
    }

    return(
        <div className="m-container m-enquire-now m-offer-modal m-form-pos-btm p-0">
            <span className="m-close" onClick={() => handleOfferClose(state => !state)}>x</span>
            <div className="m-offer-box">
                <div className="m-offer-txt">
                    <span className="m-offer-heading">Limited time offer by <strong>{navOffer[1]}</strong> <strong> {navOffer[3]} off &thinsp;</strong></span>
                    Offer ends in  
                    <p className="mt-10">
                        <OfferTimer timerDate={navOffer[0]} cssClass='m-time' type="modal" />
                    </p>
                </div>
            </div>
            <div className="pl-15 pr-15 mt-20">
                <h2 className="m-heading2">Avail offer</h2>
                <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>
                    <InputField attributes={EnquireNowForm.name} register={register} errors={!!errors ? errors[EnquireNowForm.name.name] : false} />

                    <InputField attributes={inboxForm.emailCampaign} register={register} errors={!!errors ? errors[inboxForm.emailCampaign.name] : ''} />

                    <div className="d-flex">
                            <SelectBox attributes={EnquireNowForm.country_code} register={register} />
                            <InputField attributes={inboxForm.mobile} register={register} errors={!!errors ? errors[inboxForm.mobile.name] : ''} />
                    </div>
                    
                    <div className="m-form-group">
                        <button className="btn-blue">Avail offer now!</button>
                    </div>
                </form>
                <div className="m-brand-partner">
                    <strong><span>Course offered by</span></strong>
                    <figure>
                    <img src={navOffer[6]} alt="Cambridge Assessment English" />
                    </figure>
                    <span>*T&C applied, valid only on select courses</span>
                </div>
            </div>
        </div>
    )
}

export default OfferModal;