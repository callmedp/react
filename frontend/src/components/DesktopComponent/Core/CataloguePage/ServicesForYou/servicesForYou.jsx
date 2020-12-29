import React from 'react';
import './servicesForYou.scss';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

const OurVendors = (props) => {

    const { recommendedServices } = useSelector( store => store.catalog );
    

    return (
        <section id="services" className="container mt-30" data-aos="fade-up">
            <div className="row">
                <h2 className="heading2 text-center mb-30 mx-auto">Services for you</h2>
                <div className="col-sm-12 d-flex">
                    {
                        recommendedServices?.map((service, index) => {
                            return (
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
                            )
                        })
                    }    
                </div>
            </div>
        </section>
    )
}

export default OurVendors;