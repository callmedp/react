import React from 'react';
import './footer.scss'
import { siteDomain } from 'utils/domains'; 

const Footer = (props) => {
    return(
        <footer className="m-container m-footer" data-aos="fade-up">
            <span className="m-footer__social mb-10">
                <a href="https://www.facebook.com/shinelearningdotcom/">
                    <figure className="micon-facebook"></figure>
                </a>
                <a href="https://www.linkedin.com/showcase/13203963/">
                    <figure className="micon-linkedin"></figure>
                </a>
                <a href="https://twitter.com/shinelearning">
                    <figure className="micon-twitter"></figure>
                </a>
            </span>

            <p className="m-footer__txt">Copyright © { new Date().getFullYear()}  HT Media Limited. <br /><a href={`${siteDomain}/privacy-policy/`}>Privacy Policy</a> |  <a href={`${siteDomain}/tnc/`}>Terms &amp; Conditions</a></p>
        </footer>
    )
}

export default Footer;