import React from 'react';
import './servicesForYou.scss';
import { useSelector } from 'react-redux';
import { resumeShineSiteDomain } from 'utils/domains';

const OurVendors = (props) => {

    const { popularServices } = useSelector( store => store.popularServices );
    

    return (
        <section id="services" className="container mt-30" data-aos="fade-up">
            <div className="row">
                <h2 className="heading2 text-center mb-30 mx-auto">Services for you</h2>
                <div className="col-sm-12 d-flex">
                    {
                        popularServices?.slice(0,4).map((service, index) => {
                            return (
                                <div className="col-sm-3" key={service.id}>
                                    <div className="services-foryou">
                                        <h3 className="heading3">{service.name}</h3>
                                        <p>{service.description}</p>
                                        <span className="d-flex">
                                            <a href={`${resumeShineSiteDomain}${service.url}`}>Know more</a>
                                            <figure >
                                            <img height="30" width="40"  src={service.img} alt={service.img_alt} />
                                            </figure>
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