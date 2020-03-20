import React from  'react';


export default function Footer() {
    return (

<footer className="mt-40">
    <div className="container">
      <nav className="navbar navbar-expand-lg">
        <div className="collapse navbar-collapse" id="navbarText">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <a className="nav-link" href="/about-us">About Us</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/privacy-policy">Privacy Policy</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/tnc">Terms & Conditions</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/contact-us">Contact Us</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/disclaimer">Disclaimer</a> 
            </li>
          </ul>
          <span className="navbar-text social-icon">
            <a href="https://www.facebook.com/shinelearningdotcom/" className="b4-icon-facebook"></a>
            <a href="https://www.linkedin.com/showcase/13203963/" className="b4-icon-linkedin"></a>
            <a href="https://twitter.com/shinelearning" className="b4-icon-twitter"></a>
          </span>
        </div>
      </nav>
      <div className="d-flex justify-content-between align-items-center mt-20">
        <div className="secure-payment">
          <figure className="b4-icon-secure mr-20"></figure>
          <span>
            <strong>100% Secure Payment</strong>
            All major credit & debit cards accepted
          </span>
        </div>
        <div className="payment-option">
            Payment options
            <figure className="b4-icon-payment-option"></figure>
        </div>
        <div className="copyright">
            Copyright © 2019 HT Media Limited.
        </div>
      </div>
    </div>
</footer>
    )
}