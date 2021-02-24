import React, {useState} from 'react';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import { shineDomain } from '../../../../../../utils/domains.js';
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
                                <div className="m-services-foryou__list">
                                    <h3 className="m-heading3">{service.title}</h3>
                                    <p>{service.about}</p>
                                    <span className="d-flex">
                                        <Link to={`${service.url}`}>Know more</Link>
                                        <figure className="micon-service1"></figure>
                                    </span>
                                </div>
                    )})}
                </Slider>
            </div>
    )
}

export default RecommendServices;