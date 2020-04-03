import React, {Component} from 'react';
import './footer.scss'

export default function Footer(){
        return(
            <div>
                <footer className="footer-new">
                    <div className="content-box pb-60">
                        <div className="footer-new__smo">
                            <a href="https://www.facebook.com/shinelearningdotcom/" className="sprite1 fb-black"></a>
                            <a href="https://www.linkedin.com/showcase/13203963/" className="sprite1 linledin-black"></a>
                            <a href="https://twitter.com/shinelearning" className="sprite1 tw-black"></a>
                        </div>
                        <p className="pb-0"><a href="https://learning.shine.com/privacy-policy/">Privacy Policy</a> | <a href="https://learning.shine.com/tnc/">Terms &amp; Conditions</a></p>
                        <p className="pb-0">2020 HT Media Limited. All rights reserved</p>
                    </div>
                </footer>
    
            </div>
        );
}