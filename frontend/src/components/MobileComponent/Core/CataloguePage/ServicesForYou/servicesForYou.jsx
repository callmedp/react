import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './servicesForYou.scss'
import { useSelector } from 'react-redux';
import { siteDomain }  from 'utils/domains';

const ServicesForYou = (props) => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };
    const { popularServices } = useSelector( store => store.popularServices );

    return(
        <section className="m-container mt-0 mb-0 pr-0" data-aos="fade-up" id="services">
            <div className="m-services-foryou">
                <h2 className="m-heading2 text-center">Services for you</h2>
                <Slider {...settings}>
                {
                    popularServices?.slice(0,4).map((service, index) => {
                        return (
                            <div className="m-services-foryou__list" key={index}>
                                <h3 className="m-heading3">{service.name}</h3>
                                <p>{service.description}</p>
                                <span className="d-flex">
                                    <a href={`${siteDomain}${service.url}`}>Know more</a>
                                    <figure>
                                        <img src={service.img} alt={service.img_alt} />
                                    </figure>
                                </span>
                            </div>
                        )
                    })
                }
                </Slider>
            </div>
        </section>
    )
}

export default ServicesForYou;