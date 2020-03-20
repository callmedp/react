import React from  'react';


export default function Footer() {
    return (

<footer class="mt-40">
    <div class="container">
      <nav class="navbar navbar-expand-lg">
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="/about-us">About Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/privacy-policy">Privacy Policy</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/tnc">Terms & Conditions</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/contact-us">Contact Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/disclaimer">Disclaimer</a> 
            </li>
          </ul>
          <span class="navbar-text social-icon">
            <a href="https://www.facebook.com/shinelearningdotcom/" class="b4-icon-facebook"></a>
            <a href="https://www.linkedin.com/showcase/13203963/" class="b4-icon-linkedin"></a>
            <a href="https://twitter.com/shinelearning" class="b4-icon-twitter"></a>
          </span>
        </div>
      </nav>
      <div class="d-flex justify-content-between align-items-center mt-20">
        <div class="secure-payment">
          <figure class="b4-icon-secure mr-20"></figure>
          <span>
            <strong>100% Secure Payment</strong>
            All major credit & debit cards accepted
          </span>
        </div>
        <div class="payment-option">
            Payment options
            <figure class="b4-icon-payment-option"></figure>
        </div>
        <div class="copyright">
            Copyright © 2019 HT Media Limited.
        </div>
      </div>
    </div>
</footer>
    )
}