import React from 'react';
import './footer.scss';
import { siteDomain } from '../../../Utils/domains';

export default function Footer(){
        return(
            <div>
                <footer className="footer-new">
                    <div className="content-box pb-60">
                        <div className="footer-new__smo">
                            <a href="https://www.facebook.com/shinelearningdotcom/" className="sprite fb-black"> </a>
                            <a href="https://www.linkedin.com/showcase/13203963/" className="sprite linledin-black"> </a>
                            <a href="https://twitter.com/shinelearning" className="sprite tw-black"> </a>
                        </div>
                        <p className="pb-0"><a href={`${siteDomain}/privacy-policy/`}>Privacy Policy</a> | <a href={`${siteDomain}/tnc/`}>Terms &amp; Conditions</a></p>
                        <p className="pb-0">2020 HT Media Limited. All rights reserved</p>
                    </div>
                </footer>
    
            </div>
        );
}