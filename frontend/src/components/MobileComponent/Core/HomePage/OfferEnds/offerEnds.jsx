import React from 'react';
import './offerEnds.scss';

const OfferEnds = (props) => {
    return(
        <section className="m-offer-ends mt-0 mb-0">
            <p><span>SALE ENDS TODAY  |</span>  FLAT 25% OFF  <br />Offer ends in  <strong>11</strong> H <strong>27</strong> M <strong>44</strong> S</p>
            <button className="m-close-offer micon-close"></button>
        </section>
    )
}

export default OfferEnds;