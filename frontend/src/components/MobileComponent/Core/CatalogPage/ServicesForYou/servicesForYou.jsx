import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './servicesForYou.scss'

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
    return(
        <section className="m-container mt-0 mb-0" data-aos="fade-up">
            <div className="m-services-foryou">
                <h2 className="m-heading2 text-center">Services for you</h2>
                <Slider {...settings}>
                    <div className="m-services-foryou__list">
                        <h3 className="m-heading3">Resume Writing</h3>
                        <p>Resume written by experts to increase your profile visibility</p>
                        <span className="d-flex">
                            <Link to={"#"}>Know more</Link>
                            <figure className="micon-service1"></figure>
                        </span>
                    </div>
                    <div className="m-services-foryou__list">
                        <h3 className="m-heading3">Featured Profile</h3>
                        <p>Appear on top when Recruiters search for best candidates</p>
                        <span className="d-flex">
                            <Link to={"#"}>Know more</Link>
                            <figure className="micon-service2"></figure>
                        </span>
                    </div>
                    <div className="m-services-foryou__list">
                        <h3 className="m-heading3">Jobs on the Move</h3>
                        <p>Get personalized job recommendations from all the job portals on your Whatsapp</p>
                        <span className="d-flex">
                            <Link to={"#"}>Know more</Link>
                            <figure className="micon-service3"></figure>
                        </span>
                    </div>
                    <div className="m-services-foryou__list">
                        <h3 className="m-heading3">Application Highlighter</h3>
                        <p>Get your Job Application noticed among others</p>
                        <span className="d-flex">
                            <Link to={"#"}>Know more</Link>
                            <figure className="micon-service4"></figure>
                        </span>
                    </div>
                </Slider>
            </div>
        </section>
    )
}

export default ServicesForYou;