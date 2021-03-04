import React, {useState} from 'react';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import { shineDomain, siteDomain } from '../../../../../../utils/domains.js';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import './shineServices.scss';
import { showSwal } from 'utils/swal';


const RecommendServices = (props) => {
    const { services, settings } = props;

    return (
            <div className="m-services-foryou ml-10n mt-40">
                <h2 className="m-heading2 ml-10">Recommended services</h2>
                <Slider {...settings}>
                    { services?.map((service, index) => {
                            return (
                                <div className="m-services-foryou__list" key={index}>
                                    <h3 className="m-heading3">{service.title?.length > 50 ? service.title?.slice(0, 50) + '...' :  service.title}</h3>
                                    <p>{ service.about?.length > 85 ? service.about?.slice(0, 85) + '...' :  service.about }</p>
                                    <span className="d-flex">
                                        <a href={`${siteDomain}${service.url}`}>Know more</a>
                                        <figure>
                                            <img src={service?.imgUrl} alt={service?.imgAlt} />
                                        </figure>
                                    </span>
                                </div>
                    )})}
                </Slider>
            </div>
    )
}

export default RecommendServices;