import React, {useState} from 'react';
import './servicesForYou.scss';
import { Link } from 'react-router-dom';

   
const OurVendors = (props) => {
    return(
        <section id="services" className="container mt-30" data-aos="fade-up">
            <div className="row"> 
                <h2 className="heading2 text-center mb-30 mx-auto">Services for you</h2>
                <div className="col-sm-12 d-flex">
                    <div className="col-sm-3">
                        <div className="services-foryou">
                            <h3 className="heading3">Resume Writing</h3>
                            <p>Resume written by experts to increase your profile visibility</p>
                            <span className="d-flex">
                                <Link to={"#"}>Know more</Link>
                                <figure className="icon-service1"></figure>
                            </span>
                        </div>
                    </div>
                    <div className="col-sm-3">
                        <div className="services-foryou">
                            <h3 className="heading3">Featured Profile</h3>
                            <p>Appear on top when Recruiters search for best candidates</p>
                            <span className="d-flex">
                                <Link to={"#"}>Know more</Link>
                                <figure className="icon-service2"></figure>
                            </span>
                        </div>
                    </div>
                    <div className="col-sm-3">
                        <div className="services-foryou">
                            <h3 className="heading3">Jobs on the Move</h3>
                            <p>Get personalized job recommend -ations from all the job portals on your Whatsapp</p>
                            <span className="d-flex">
                                <Link to={"#"}>Know more</Link>
                                <figure className="icon-service3"></figure>
                            </span>
                        </div>
                    </div>
                    <div className="col-sm-3">
                        <div className="services-foryou">
                            <h3 className="heading3">Application Highlighter</h3>
                            <p>Get your Job Application noticed among others</p>
                            <span className="d-flex">
                                <Link to={"#"}>Know more</Link>
                                <figure className="icon-service4"></figure>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default OurVendors;