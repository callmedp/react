import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './bannerSlider.scss';

const BannerSlider = (props) => {
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
        <section className="m-banner-slider">
            <Slider {...settings}>
                <div className="m-banner-slider__txt">
                    <figure className="micon-round-arrow"></figure>
                    <p>
                         <strong>26% Annual Growth</strong> for cloud related opportunities In IT Sector
                    </p>
                </div>
                <div className="m-banner-slider__txt">
                    <figure className="micon-round-arrow"></figure>
                    <p>
                         <strong>26% Annual Growth</strong> for cloud related opportunities In IT Sector
                    </p>
                </div>
                <div className="m-banner-slider__txt">
                    <figure className="micon-round-arrow"></figure>
                    <p>
                         <strong>26% Annual Growth</strong> for cloud related opportunities In IT Sector
                    </p>
                </div>
            </Slider>
        </section>
    );
  }

export default BannerSlider;