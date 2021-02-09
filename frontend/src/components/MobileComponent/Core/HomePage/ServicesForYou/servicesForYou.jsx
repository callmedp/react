// React Core Import
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

// Third-Party Import
import Slider from "react-slick";
import Swal from 'sweetalert2';

// Inter-App Import
import 'slick-carousel/slick/slick.css';
import './servicesForYou.scss'
import { siteDomain } from 'utils/domains';

// API Import


const ServicesForYou = (props) => {
    const jobAssistanceLists = useSelector(store => store?.jobAssistance?.jobAssistanceServices)

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

    return (
        <section className="m-container mt-0 mb-0 pr-0" data-aos="fade-up">
            <div className="m-services-foryou">
                <h2 className="m-heading2-home text-center mb-5">Job assistance services</h2>
                <p className="fs-13 text-center">Find your next job faster by using our services</p>
                <Slider {...settings}>

                    {
                        jobAssistanceLists?.map((job, index) => {
                            return (
                                <div className="m-services-foryou__list" key={index}>
                                    <h3 className="m-heading3">{ job?.heading }</h3>
                                    <p>{ job?.description?.length > 61 ? job?.description?.slice(0, 58) + '...' : job?.description }</p>
                                    <span className="d-flex">
                                        <a href={`${siteDomain}${job?.url}`}>Know more</a>
                                        <figure className={`micon-service${index + 1}`}></figure>
                                    </span>
                                </div>
                            )
                        })
                    }

                    {/* <div className="m-services-foryou__list">
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
                    </div> */}
                </Slider>
            </div>
        </section>
    )
}

export default ServicesForYou;