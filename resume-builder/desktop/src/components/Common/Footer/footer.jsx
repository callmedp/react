import React from 'react';
import './footer.scss'

export default function Footer(props) {

    
    const handleFooterClick = () =>{
        props.sendTrackingInfo('exit_resume_builder',1)
    }

    return (
        <footer>
            <div className="container">
                <div className="container--footer-links">
                    <a href="/about-us" onClick={handleFooterClick}>About Us</a> 
                    <a href="/privacy-policy" onClick={handleFooterClick}>Privacy Policy</a> 
                    <a href="/tnc" onClick={handleFooterClick}>Terms & Condition</a> 
                    <a href="/contact-us" onClick={handleFooterClick}>Contact us</a>
                </div>
                <div className="container--footer-txt">Copyright © 2020 HT Media Limited.</div>
            </div>
        </footer>
    )
}


