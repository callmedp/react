import React from 'react';
import './banner.scss';
import Carousel from 'react-bootstrap/Carousel';
import SearchBar from '../../../Common/Header/SeachBar/SearchBar.jsx';
import { imageUrl } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';

const HomeBanner = () => {
    const sendLearningTracking = useLearningTracking();

    const goToCareerGuidance = () => {
        MyGA.SendEvent('ln_career_guidance','ln_career_guidance', 'ln_click_career_guidance', 'career_guidance','', false, true);
        
        sendLearningTracking({
            productId: '',
            event: 'homepage_banner_career_guidance_clicked',
            pageTitle:'homepage',
            sectionPlacement: 'banner_career_guidance',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })

        window.location.href = `${siteDomain}/user-intent`;
    }

    return (
       <header className="container-fluid pos-rel home-bg">
           
            <div className="row">
                <div className="container home-header-content mt-30">
                    <div className="w-75">
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
                            <SearchBar place="banner" placeHolder = 'Search course, assessment...' isHomepage={true} pageTitle={'homepage'} />
                            {/* <form className="form-inline top-search my-2 my-lg-0">
                                <input className="form-control top-input" type="search" placeholder="Search courses" aria-label="Search" />
                                <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
                            </form> */}
                            OR
                            <a className="btn btn-gradient ml-10" onClick={() => goToCareerGuidance()}>GET CAREER GUIDANCE <figure className="icon-arrow-right ml-10"></figure></a>
                        </div>
                    </div>

                    <div className="banner-home-right">
                        <div className="banner-right-img">
                            <span className="home-banner-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/home-animation-header1.svg`} />
                            </span>
                            
                            <span className="home-banner-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                                <img id="start" src={`${imageUrl}desktop/home-animation-header3.svg`} />
                            </span>
                            <span className="home-banner-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/home-animation-header4.svg`} />
                            </span>
                            {/* <span className="home-banner-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000" id="bounce">
                                <img src={`${imageUrl}desktop/home-animation-header5.svg`} />
                            </span> */}
                            <span className="home-banner-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900" data-aos-duration="1000" id="start">
                                <img src={`${imageUrl}desktop/home-animation-header2.png`} />
                            </span>
                            <span className="home-banner-tween7" data-aos="fade-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1100" data-aos-duration="1000" data-aos-anchor="#start">
                                <img src={`${imageUrl}desktop/home-animation-header6.png`} />
                            </span>
                            <span className="home-banner-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/home-animation-header2.png`} />
                            </span>
                        </div>
                    </div>

                </div>
            </div>

            
       </header> 
    )
}

export default HomeBanner;