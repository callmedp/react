import React from 'react';
import './footer.scss';


const Footer=(props)=> {
  return (

    <footer>
      <div className="container">
        <div className="row mb-4">
          <div className="footer-links col-sm-8">
            <a href="https://learning.shine.com/about-us">About Us</a>
            <a href="#banner">Partners</a>
            <a href="https://learning.shine.com/privacy-policy/">Privacy Policy</a>
            <a href="https://learning.shine.com/tnc/">Terms &amp; Conditions</a>
            <a href="https://learning.shine.com/contact-us">Contact Us</a>
          </div>

          <div className="footer-social col-sm-4">
            <a aria-label="follow us on facebook" className="sprite1 facebook mr-10" href="https://www.facebook.com/shinelearningdotcom/">&nbsp;</a>
            <a aria-label="follow us on linkedin" className="sprite1 linkedin mr-10" href="https://www.linkedin.com/showcase/shine-learning/">&nbsp;</a>
            <a aria-label="follow us on twitter" className="sprite1 twitter" href="https://twitter.com/shinelearning">&nbsp;</a>
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

export default  Footer;