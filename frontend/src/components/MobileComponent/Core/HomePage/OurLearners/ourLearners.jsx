import React, { Component } from "react";
import './ourLearners.scss';

const OurVendors = (props) => {
    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <h2 className="m-heading2-home text-center mx-auto">Our learners are now at these amazing places</h2>
            <div className="m-our-learners-slider">
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-google.png" className="img-fluid" alt="Google" />
                        </figure>
                    </div>
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-people-strong.png" className="img-fluid" alt="People Strong" />
                        </figure>
                    </div>
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-infosys.png" className="img-fluid" alt="Infosys" />
                        </figure>
                    </div>
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-fujitsu.png" className="img-fluid" alt="Fujitsu" />
                        </figure>
                    </div>
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-ibm.png" className="img-fluid" alt="IBM" />
                        </figure>
                    </div>
                    <div className="m-our-learners-slider__txt">
                        <figure>
                            <img src="/media/images/mobile/logo-genpact.png" className="img-fluid" alt="Genpact" />
                        </figure>
                    </div>
            </div>
        </section>
    )
}
   
export default OurVendors;