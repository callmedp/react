import React, {useState} from 'react';
import Toast from 'react-bootstrap/Toast';
import './offerEnds.scss';
import OfferModal from '../../../Common/Modals/offerModal';
import OfferTimer from 'utils/OfferTimer';

const OfferEnds = (props) => {
  const { navOffer } = props;
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [offerStatus, setOfferStatus] = useState(false);
  const [showMainOffer, setShowMainOffer] = useState(true);

  return(
    <>
      {
        showMainOffer &&
        <div>
          <Toast className="offer-ends">
            <Toast.Header closeButton={false}>
              <p className="flex-1">
                limited time offer by&nbsp;<strong>{navOffer[1]}&nbsp;</strong>   |  {navOffer[3]} OFF  |  Offer ends in
                  <OfferTimer timerDate={navOffer[0]} cssClass='time' type="main" />
                <em onClick={handleShow} className="btn btn-inline btn-outline-primary">Avail offer</em>
              </p>
              <span className="close mr-3" onClick={() => setShowMainOffer(false)}>x</span>
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