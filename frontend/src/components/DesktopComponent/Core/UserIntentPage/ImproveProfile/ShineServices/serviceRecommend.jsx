import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import { shineDomain, siteDomain } from '../../../../../../utils/domains.js';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import './shineServices.scss';


const RecommendServices = (props) => {
    const { services } = props;

    return (
        <>
            <h2 className="heading3 mt-50">Recommended services</h2>
            <div className="w-70">
                <div className="row recommend-services">
                { services?.map((service, index) => {
                return (
                    <div className="col">
                        <Link to={`${siteDomain}${service.url}`}>
                            <div className="services-foryou">
                                <h3 className="heading3">{service.title?.length > 50 ? service.title?.slice(0, 50) + '...' :  service.title}</h3>
                                <p>{ service.about?.length > 85 ? service.about?.slice(0, 85) + '...' :  service.about }</p>
                                <span className="d-flex">
                                    <a href={`${siteDomain}${service.url}`}>Know more</a>
                                    <figure>
                                        <img src={service?.imgUrl} alt={service?.imgAlt} />
                                    </figure>
                                </span>
                            </div>
                        </Link>
                    </div>
                )})}
                </div>
            </div>
        </>
    )
}

export default RecommendServices;