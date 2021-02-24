import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import { shineDomain } from '../../../../../../utils/domains.js';
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
                        <div className="services-foryou">
                            <h3 className="heading3">{service.title}</h3>
                            <p>{service.about}</p>
                            <span className="d-flex">
                                <Link to={`${service.url}`}>Know more</Link>
                                <figure className={"icon-service1"}></figure>
                            </span>
                        </div>
                    </div>
                )})}
                </div>
            </div>
        </>
    )
}

export default RecommendServices;