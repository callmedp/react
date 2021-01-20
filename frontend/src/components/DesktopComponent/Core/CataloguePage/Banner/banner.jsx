import React from 'react';
import { Link as LinkScroll } from 'react-scroll'
import { imageUrl } from 'utils/domains';
import './banner.scss';


const CatalogBanner = (props) => {
    return (
       <header className="container-fluid pos-rel catalog-bg">
            <div className="row">
                <div className="container catalog-header-content mt-30">
                    <div className="w-50 mb-50">
                        <h1 className="heading1" data-aos="fade-right">
                            <strong>India's largest</strong> e-learning platform
                        </h1>
                        <p>Join the club of 4mn learners with our partners like Skillsoft, ACCA etc</p>
                        <div className="d-flex w-100 mt-10">
                            <LinkScroll to="all-categories"  isDynamic={true} spy={true} offset={-35} className="btn btn-outline-white mr-10">View categories</LinkScroll>
                            <LinkScroll to="recommended-services" isDynamic={true} spy={true} offset={-70} className="btn btn-outline-white">View services</LinkScroll>
                        </div>
                    </div>
                    <div className="catalog-banner-right">
                        <div className="banner-right-img">
                            <span className="catalog-banner-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/catalog-animation-header1.svg`} />
                            </span>
                            <span className="catalog-banner-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/catalog-animation-header2.svg`} />
                            </span>
                            <span className="catalog-banner-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/catalog-animation-header3.svg`} />
                            </span>
                            <span className="catalog-banner-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/catalog-animation-header4.svg`} />
                            </span>
                            <span className="catalog-banner-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900" data-aos-duration="1000">
                                <img src={`${imageUrl}desktop/catalog-animation-header5.svg`} />
                            </span>
                        </div>
                    </div>
                </div>
            </div>
       </header> 
    )
}

export default CatalogBanner;