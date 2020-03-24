import React from  'react';
import './footer.scss';


export default function Footer() {
    return (

<footer>
  <div className="container">
      <div className="row mb-4">
        <div className="footer-links col-sm-8">
          <a href="/about-us">About Us</a>
          <a href="#">Partners</a>
          <a href="/privacy-policy">Privacy Policy</a>
          <a href="/tnc">Terms &amp; Conditions</a>
          <a href="/contact-us">Contact Us</a>
        </div>
          
        <div className="footer-social col-sm-4">
          <a aria-label="follow us on facebook" className="sprite1 facebook mr-10" href="#"></a>
          <a aria-label="follow us on linkedin" className="sprite1 linkedin mr-10" href="#"></a>
          <a aria-label="follow us on twitter" className="sprite1 twitter" href="#"></a>
        </div>
      </div>
      <hr></hr>

      <div className="row my-5">
            <div className="col-sm-4">
              <div className="secure-payment">
                <figure className="sprite1 secure-icon mr-3"></figure>
                <span className="secure-text"><strong className="d-block">100% Secure Payment</strong>
                All major credit &amp; debit cards accepted</span>
              </div>
            </div>
                <div className="col-sm-5">
                  <div className="payment-options">
                    <figure className="payment-option-txt">Payment options</figure>
                    <span className="sprite1 payment-option-bg"></span>
                  </div>
                </div>
                <div className="col-sm-3">
                  <div className="h-100 d-flex align-items-center">
                    <span className="copyright-txt mt-20">Copyright © 2020 HT Media Limited.</span>
                  </div>
                </div>
          </div>
  </div>
</footer>
    )
}