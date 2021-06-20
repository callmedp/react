import React from 'react';
import './footer.scss'
import { siteDomain } from 'utils/domains'; 
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const Footer = (props) => {
    const { pageType } = props;
    const sendLearningTracking = useLearningTracking();

    const footerTracking = (title, ln_title, event_clicked, name, val, val1, val2) => {
        let name_joined = name.replace(/ /gi, '_');
        MyGA.SendEvent(title, ln_title, event_clicked, name_joined, val, val1, val2);

        sendLearningTracking({
            productId: '',
            event: `${pageType}_${name_joined}_footer_clicked`,
            pageTitle: pageType,
            sectionPlacement: 'footer',
            eventCategory: name_joined,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return(
        <footer className={`m-container m-footer ${ (pageType === 'homePage' || 'course_detail') ? 'pb-100' : '' }`}>
            <span className="m-footer__social mb-10">
                <a href="https://www.facebook.com/shinelearningdotcom/" onClick={() => footerTracking('social_media_follow','ln_social_media_follow', 'ln_facebook', `${pageType}`,'', false, true)}>
                    <figure className="micon-facebook"></figure>
                </a>
                <a href="https://in.linkedin.com/company/shinelearning" onClick={() => footerTracking('social_media_follow','ln_social_media_follow', 'ln_linkedin', `${pageType}`,'', false, true)}>
                    <figure className="micon-linkedin"></figure>
                </a>
                <a href="https://twitter.com/shinelearning" onClick={() =>  footerTracking('social_media_follow','ln_social_media_follow', 'ln_twitter', `${pageType}`,'', false, true)}>
                    <figure className="micon-twitter"></figure>
                </a>
            </span>

            <p className="m-footer__txt">Copyright © { new Date().getFullYear()} HT Media Limited. <br /><a href={`${siteDomain}/privacy-policy/`} onClick={() => footerTracking(`${pageType}_footer`,`ln_${pageType}_footer`, `ln_${pageType}_footer_clicked`, 'Privacy Policy','', false, true)}>Privacy Policy</a> |  <a href={`${siteDomain}/tnc/`} onClick={() => footerTracking(`${pageType}_footer`,`ln_${pageType}_footer`, `ln_${pageType}_footer_clicked`, 'Terms & Conditions','', false, true)}>Terms &amp; Conditions</a></p>
        </footer>
    )
}

export default Footer;