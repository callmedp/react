import React, {useState} from 'react';
import OfferTimer from 'utils/OfferTimer';
import './offerEnds.scss';
import OfferModal from '../../../Common/Modals/OfferModal';
import ThanksModal from '../../../Common/Modals/ThanksModal';
import useLearningTracking from 'services/learningTracking';

const OfferEnds = (props) => {
    const { navOffer, showOffer, setShowOffer, offerStatus, setOfferStatus } = props;
    const handleOfferClose = () => setShowOffer(false);
    const handleOfferShow = () => setShowOffer(true);
    const [showMainOffer, setShowMainOffer] = useState(true);
    const sendLearningTracking = useLearningTracking();

    const trackOffer = () => {
        handleOfferShow(state => !state);
    
        sendLearningTracking({
          productId: '',
          event: `homepage_banner_offer_${navOffer[1] || navOffer[2] || ''}_clicked`,
          pageTitle:`homepage`,
          sectionPlacement:'banner_offer',
          eventCategory: navOffer[1] || navOffer[2] || '',
          eventLabel: '',
          eventAction: 'click',
          algo: '',
          rank: ''
        })
    }

    return(
        <>
            {
                showMainOffer &&
                <section className="m-offer-ends mt-0 mb-0">
                    <p>
                        <span className="m-offer-heading"><span>Limited time offer by <strong>{navOffer[1]}&nbsp;</strong> |</span>  {navOffer[3]} OFF &emsp;</span>
                        Offer ends in
                        <OfferTimer timerDate={navOffer[0]} cssClass='m-time' type="main" />
                        <em className="btn-blue-outline mt-5" onClick={() => {trackOffer()}}>Avail offer</em>
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