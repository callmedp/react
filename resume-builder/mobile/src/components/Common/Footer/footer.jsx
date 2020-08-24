import React, {Component} from 'react';
import './footer.scss'
import { removeTrackingInfo } from '../../../Utils/common';

export default function Footer(props) {

    const handleFooterClick = () => {
        props.sendTrackingInfo('resume_builder_exit',1)
        removeTrackingInfo()
    }

        return (
            <footer className="footer">
                <ul className="footer__items">
                    <li className="footer__item"><a href="/privacy-policy" onClick={handleFooterClick}>Privacy Policy</a></li>
                    <li className="footer__item"><a href="/tnc" onClick={handleFooterClick}>Terms & Condition</a></li>
                    <li className="footer__item"><a href="/contact-us" onClick={handleFooterClick}>Contact us</a></li>
                </ul>
                <p>Copyright © 2020 HT Media Limited. All rights reserved</p>
            </footer>
        )

}
