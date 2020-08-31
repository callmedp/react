import React from 'react';
import './footer.scss'

export default function Footer(props) {

    const handleFooterClick = () => {
        props.sendTrackingInfo('exit_resume_builder',1)
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
