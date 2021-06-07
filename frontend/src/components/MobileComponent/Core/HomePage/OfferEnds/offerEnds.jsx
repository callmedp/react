import React, {useState} from 'react';
import OfferTimer from 'utils/OfferTimer';
import './offerEnds.scss';
import OfferModal from '../../../Common/Modals/OfferModal';
import ThanksModal from '../../../Common/Modals/ThanksModal';

const OfferEnds = (props) => {
    const { navOffer } = props;
    const [showOffer, setShowOffer] = useState(false);
    const handleOfferClose = () => setShowOffer(false);
    const handleOfferShow = () => setShowOffer(true);
    const [offerStatus, setOfferStatus] = useState(false);
    const [showMainOffer, setShowMainOffer] = useState(true);

    return(
        <>
            {
                showMainOffer &&
                <section className="m-offer-ends mt-0 mb-0">
                    <p>
                        <span className="m-offer-heading"><span>Limited time offer by <strong>{navOffer[1]}&nbsp;</strong> |</span>  {navOffer[3]} OFF</span>
                        Offer ends in
                        <OfferTimer timerDate={navOffer[0]} cssClass='m-time' type="main" />
                        <em className="btn-blue-outline" onClick={handleOfferShow}>Avail offer</em>
                    </p>
                    <button className="m-close-offer micon-close" onClick={() => setShowMainOffer(!showMainOffer)}></button>

                    {(showOffer && !offerStatus) && <OfferModal handleOfferClose={handleOfferClose} setOfferStatus={setOfferStatus} navOffer={navOffer}/> }

                    {
                        offerStatus && <ThanksModal setOfferStatus={setOfferStatus} />
                    }
                </section>
            }
        </>
    )
}

export default OfferEnds;