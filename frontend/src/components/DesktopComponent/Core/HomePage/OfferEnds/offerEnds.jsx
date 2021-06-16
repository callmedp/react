import React, {useState} from 'react';
import Toast from 'react-bootstrap/Toast';
import './offerEnds.scss';
import OfferModal from '../../../Common/Modals/offerModal';
import OfferTimer from 'utils/OfferTimer';
import useLearningTracking from 'services/learningTracking';

const OfferEnds = (props) => {
  const { navOffer, showMainOffer, setShowMainOffer } = props;
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [offerStatus, setOfferStatus] = useState(false);
  const sendLearningTracking = useLearningTracking();

  const trackOffer = () => {
    sendLearningTracking({
      productId: '',
      event: `homepage_banner_offer_${navOffer[1]}_clicked`,
      pageTitle:`homepage`,
      sectionPlacement:'banner_offer',
      eventCategory: navOffer[1],
      eventLabel: navOffer[1],
      eventAction: 'click',
      algo: '',
      rank: ''
    })
  }

  return(
    <>
      {
        showMainOffer &&
        <div>
          <Toast className="offer-ends">
            <Toast.Header closeButton={false}>
              <p className="flex-1">
                limited time offer by&nbsp;<strong>{navOffer[1]}&nbsp;</strong>  |  {navOffer[3]} OFF  |  Offer ends in
                  <OfferTimer timerDate={navOffer[0]} cssClass='time' type="main" />
                  <em onClick={() => {handleShow(); trackOffer()}} className="btn btn-inline btn-outline-primary">Avail offer</em>
              </p>
              <span className="icon-close mr-3" onClick={() => setShowMainOffer(false)}>x</span>
            </Toast.Header>
          </Toast>

          {
            (show && !offerStatus) && <OfferModal show={show} handleClose={handleClose} navOffer={navOffer} />
          }
        </div>
      }
    </>
  )
}

export default OfferEnds;