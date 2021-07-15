import React from 'react';
import './servicesForYou.scss';
import { useSelector } from 'react-redux';
import { siteDomain, resumeShineSiteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';

const OurVendors = (props) => {

    const { popularServices } = useSelector( store => store.popularServices );
    const sendLearningTracking = useLearningTracking();

    const handleTracking = (name, index) => {
        sendLearningTracking({
            productId: '',
            event: `catalogue_page_${name}_clicked`,
            pageTitle:'catalogue_page',
            sectionPlacement: 'services_for_you',
            eventCategory: name,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: index,
        })
    }

    return (
        <section id="recommended-services" className="container mt-30" data-aos="fade-up">
            <div className="row">
                <h2 className="heading2 text-center mb-30 mx-auto">Services for you</h2>
                <div className="col-sm-12 d-flex">
                    {
                        popularServices.slice(0,4)?.map((service, index) => {
                            return (
                                <div className="col-sm-3" key={service.id}>
                                    <div className="services-foryou">
                                        <h3 className="heading3">{service.heading?.length > 56 ? (service.heading?.slice(0,56) + '...') : service.heading}</h3>
                                        <p>{service.description?.length > 85 ? service.description?.slice(0, 85) + '...' : service.description}</p>
                                        <span className="d-flex">
                                            <a href={`${siteDomain}${service.url}`} onClick={() => handleTracking(service.heading, index)}>Know more</a>
                                            <figure >
                                                <img src={service.img} alt={service.img_alt} />
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