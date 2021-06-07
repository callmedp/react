import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import {InputField, SelectBox} from 'formHandler/desktopFormHandler/formFields';
import NeedHelpForm from 'formHandler/desktopFormHandler/formData/needHelp';
import { useForm } from "react-hook-form";
// import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
// import Loader from '../Loader/loader';
import { imageUrl } from 'utils/domains';
import '../../Core/HomePage/OfferEnds/offerEnds.scss';
import { fetchLeadManagement } from 'store/LeadManagement/actions';
import OfferTimer from 'utils/OfferTimer';

const OfferModal =(props) => {
    const { show, handleClose, timerDays, timerHours, timerMinutes, timerSeconds, navOffer } = props;
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    const [offerStatus, setOfferStatus] = useState(false);

    const onSubmit = async (values, event) => {
        values['course'] = navOffer[2];
        values['product_offer'] = true;
        values['msg'] = `${navOffer[1]} - ${navOffer[3]}`;
        values['lsource'] = 34;
        values["source"] = navOffer[2];
        values["campaign"] = 'homepage-banner';
        
        const result = await new Promise((resolve, reject) => dispatch(fetchLeadManagement({ payload: values, resolve, reject })))
        if(result.status) setOfferStatus(result.status);
    }

    return (
        <>
            {/* { reviewLoader ? <Loader /> : ''} */}
            <Modal 
                show={show} 
                onHide={handleClose}
                dialogClassName="offer-end-box"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                
                <Modal.Header closeButton>
                </Modal.Header>
                <Modal.Body>
                    { !offerStatus ?
                    <>
                        <form className="w-50" onSubmit={handleSubmit(onSubmit)}>
                            <h2 className="heading2 mb-20">Avail offer</h2>

                            <InputField attributes={NeedHelpForm.name} register={register} errors={!!errors ? errors[NeedHelpForm.name.name] : ''} />

                            <InputField attributes={NeedHelpForm.emailCampaign} register={register} errors={!!errors ? errors[NeedHelpForm.emailCampaign.name] : ''} />

                            <div className="d-flex">
                                <SelectBox attributes={NeedHelpForm.country_code} register={register} />
                                <InputField attributes={NeedHelpForm.mobile} register={register}
                                    errors={!!errors ? errors[NeedHelpForm.mobile.name] : ''} />
                            </div>
                            <button type="submit" className="btn btn-block btn-primary submit-btn mt-10 mb-20" role="button">Avail offer now!</button>

                            <div className="brand-partner">
                            <strong><span>Course offered by</span></strong>
                            <figure>
                                <img src={`${imageUrl}desktop/cambridge-logo.png`} alt="Cambridge Assessment English" />
                            </figure>
                            <span>*T&C applied, valid only on select courses</span>
                            </div>
                        </form>
                        <div className="offer-box">
                            <div className="offer-txt">
                            <span className="offer-heading">Limited time offer -<strong> {navOffer[3]} off</strong></span>
                            Offer ends in  
                            <p className="mt-10">
                                <OfferTimer timerDate={navOffer[0]} cssClass='time' type="modal" />
                            </p>
                            </div>
                        </div>
                    </>

                    :

                    <>
                        <figure>
                            <img src={`${imageUrl}desktop/thankyou-offer.png`} alt="Thank you" />
                        </figure>
                        <h2 className="heading2 mb-20 mt-20">Our expert will get in touch with you.</h2>
                    </>
                    }
                </Modal.Body>
            </Modal>
        </>
    )
}

export default OfferModal;