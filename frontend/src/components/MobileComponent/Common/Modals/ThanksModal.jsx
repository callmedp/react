import React, {useEffect} from 'react';
import './modals.scss';
import { imageUrl } from 'utils/domains';

const OfferModal = (props) => {
    const {setOfferStatus} = props;

    useEffect(() => {
        document.body.style.overflow = 'hidden';
        return ()=> document.body.style.overflow = 'unset';
    }, []);

    return(
        <div className="m-container m-enquire-now m-offer-modal m-offer-modal-thanks m-form-pos-btm p-0">
            <span className="m-close" onClick={() => setOfferStatus(state => !state)}>x</span>

            <div className="pl-15 pr-15 mt-20">
                <figure className="mb-20 mt-20">
                  <img className="w-100" src={`${imageUrl}mobile/thankyou-offer.png`} alt="Thank you" />
              </figure>
              <h2 className="m-heading2 text-center">Our expert will get in touch with you.</h2>
            </div>
        </div>
    )
}

export default OfferModal;