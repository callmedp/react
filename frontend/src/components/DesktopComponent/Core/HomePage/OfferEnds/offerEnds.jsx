import React, {useState} from 'react';
import Toast from 'react-bootstrap/Toast';
import './offerEnds.scss';

function OfferEnds() {
    const [showA, setShowA] = useState(true);
    const toggleShowA = () => setShowA(!showA);
    return(
        <Toast className="offer-ends" show={showA} onClose={toggleShowA}>
          <Toast.Header>
            <p>SALE ENDS TODAY  |  FLAT 25% OFF  |  Offer ends in  <strong>11</strong> <span>H</span> <strong>27</strong> <span>M</span> <strong>44</strong> <span>S</span></p>
          </Toast.Header>
        </Toast>
    )
}

export default OfferEnds;