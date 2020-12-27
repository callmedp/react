import React from 'react';
import './footer.scss'
import { siteDomain } from 'utils/domains'; 
import { MyGA } from 'utils/ga.tracking.js';

const Footer = (props) => {
    return(
        <footer className="m-container m-footer" data-aos="fade-up">
            <span className="m-footer__social mb-10">
                <a href="https://www.facebook.com/shinelearningdotcom/" onClick={() => MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_facebook', 'homepage','', false, true)}>
                    <figure className="micon-facebook"></figure>
                </a>
                <a href="https://www.linkedin.com/showcase/13203963/" onClick={() => MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_linkedin', 'homepage','', false, true)}>
                    <figure className="micon-linkedin"></figure>
                </a>
                <a href="https://twitter.com/shinelearning" onClick={() =>  MyGA.SendEvent('social_media_follow','ln_social_media_follow', 'ln_twitter', 'homepage','', false, true)}>
                    <figure className="micon-twitter"></figure>
                </a>
            </span>

            <p className="m-footer__txt">Copyright © { new Date().getFullYear()} HT Media Limited. <br /><a href={`${siteDomain}/privacy-policy/`} onClick={() => MyGA.SendEvent('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Privacy Policy','', false, true)}>Privacy Policy</a> |  <a href={`${siteDomain}/tnc/`} onClick={() => MyGA.SendEvent('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Terms & Conditions','', false, true)}>Terms &amp; Conditions</a></p>
        </footer>
    )
}

export default Footer;