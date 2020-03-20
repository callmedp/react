import React from 'react';

export default function footer() {
    return(


        <div>
            <footer className="footer-new">
                <div className="content-box pb-60">
                    <div className="footer-new__smo">
                        <a href="https://www.facebook.com/shinelearningdotcom/" className="sprite fb-black"></a>
                        <a href="https://www.linkedin.com/showcase/13203963/" className="sprite linledin-black"></a>
                        <a href="https://twitter.com/shinelearning" className="sprite tw-black"></a>
                    </div>
                    <p className="pb-0"><a href="/privacy-policy">Privacy Policy</a> | <a href="/tnc">Terms &amp; Conditions</a></p>
                    <p className="pb-0">2020 HT Media Limited. All rights reserved</p>
                </div>
            </footer>


            <div className="call-to-action">
                <div className="d-flex justify-content-between">
                    <div className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                        <i className="sprite upload mr-5"></i> Upload resume                                
                        <input className="file-upload__input" type="file" name="file"></input>
                    </div>

                    <a href="#" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite export mr-5"></i>
                    Export from shine.com
                    </a>
                </div>
            </div>
            
        </div>
    );
}