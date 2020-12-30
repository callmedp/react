import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './servicesForYou.scss'
import { useSelector } from 'react-redux';

const ServicesForYou = (props) => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };
    const { popularServices } = useSelector( store => store.catalogue );

    return(
        <section className="m-container mt-0 mb-0" data-aos="fade-up" id="services">
            <div className="m-services-foryou">
                <h2 className="m-heading2 text-center">Services for you</h2>
                <Slider {...settings}>
                {
                    popularServices?.map((service, index) => {
                        return (
                            <div className="m-services-foryou__list" key={index}>
                                <h3 className="m-heading3">{service.name}</h3>
                                <p>Resume written by experts to increase your profile visibility</p>
                                <span className="d-flex">
                                    <a href={service.url}>Know more</a>
                                    <figure className="micon-service1"></figure>
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