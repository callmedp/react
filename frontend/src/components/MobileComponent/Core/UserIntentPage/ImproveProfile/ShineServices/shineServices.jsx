import React from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import './shineServices.scss';

const ShineServices = (props) => {
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
    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-completed" to={"#"}>2</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <h2 className="m-heading3 mt-20">Get an edge over others with shine services</h2>
                <div className="m-shine-services mt-20">
                    <figure className="micon-upload-resume"></figure>
                    <p>Updated resume increases the chances of getting more opportunities. 
                        <Link to={"#"} className="mt-10">Upload latest resume</Link>
                    </p>
                    
                </div>
                <div className="m-shine-services mt-20">
                    <figure className="micon-update-profile"></figure>
                    <p>Update your profile to get customised career recommendation 
                        <Link to={"#"} className="mt-10">Update your profile</Link>
                    </p>
                </div>
                
                <div className="m-services-foryou ml-10n mt-40">
                    <h2 className="m-heading2 ml-10">Recommended services</h2>
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
            </div>
        </section>
    )
}

export default ShineServices;