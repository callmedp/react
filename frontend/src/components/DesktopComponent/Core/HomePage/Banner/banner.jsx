import React from 'react';
import { Link } from 'react-router-dom';
import './banner.scss';
import Carousel from 'react-bootstrap/Carousel';
import Breadcrumb from 'react-bootstrap/Breadcrumb';

const HomeBanner = (props) => {
    return (
       <header className="container-fluid pos-rel home-bg">
           
            <div className="row">
                <div className="container home-header-content mt-30">
                    <div className="w-50">
                        <h1 className="heading1 mt-20" data-aos="fade-right">
                            <strong>Learn the right skills,</strong> be future ready
                        </h1>
                        <div className="banner-txt mt-30">
                            <Carousel fade={true}>
                                <Carousel.Item>
                                    <strong>
                                        <figure className="icon-become-expert1 mr-10"></figure> <span>Become an expert</span> and get ready for the future 
                                    </strong>    
                                </Carousel.Item>
                                <Carousel.Item>
                                    <strong>
                                        <figure className="icon-become-expert2 mr-10"></figure> To reach the <span> next step in your career ladder</span>
                                    </strong>    
                                </Carousel.Item>
                                <Carousel.Item>
                                    <strong>
                                        <figure className="icon-become-expert3 mr-10"></figure> <span>Create a brand</span> for yourself, differentiating yourself
                                    </strong>    
                                </Carousel.Item>
                            </Carousel>
                        </div>
                        <div className="banner-search mt-20">
                            <form className="form-inline top-search my-2 my-lg-0">
                                <input className="form-control top-input" type="search" placeholder="Search courses" aria-label="Search" />
                                <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
                            </form>
                            {/* OR
                            <Link to={"#services"} className="btn btn-gradient ml-10">GET CAREER GUIDANCE <figure className="icon-arrow-right ml-10"></figure></Link> */}
                        </div>
                    </div>

                    <div className="banner-home-right">
                        <div className="banner-right-img">
                            <span className="home-banner-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                                <img src="./media/images/desktop/home-animation-header1.svg" />
                            </span>
                            <span className="home-banner-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                                <img src="./media/images/desktop/home-animation-header2.png" />
                            </span>
                            <span className="home-banner-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                                <img id="start" src="./media/images/desktop/home-animation-header3.svg" />
                            </span>
                            <span className="home-banner-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000">
                                <img src="./media/images/desktop/home-animation-header4.svg" />
                            </span>
                            {/* <span className="home-banner-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000" id="bounce">
                                <img src="./media/images/desktop/home-animation-header5.svg" />
                            </span> */}
                            <span className="home-banner-tween6" data-aos="fade-zoom-in" data-aos-easing="ease-in-back-out" data-aos-offset="0" data-aos-delay="1500" data-aos-duration="1500" id="start">
                                <img src="./media/images/desktop/home-animation-header2.png" />
                            </span>
                            <span className="home-banner-tween7" data-aos="fade-zoom-in" data-aos-easing="ease-in-back-out" data-aos-offset="0" data-aos-delay="2500" data-aos-duration="2500" data-aos-anchor="#start">
                                <img src="./media/images/desktop/home-animation-header6.png" />
                            </span>

                        </div>
                    </div>

                </div>
            </div>

            
       </header> 
    )
}

export default HomeBanner;