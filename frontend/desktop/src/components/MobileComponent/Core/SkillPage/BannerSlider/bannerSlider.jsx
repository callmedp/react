import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './bannerSlider.scss';
import { useSelector } from "react-redux";

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
    const { featuresList } = useSelector( store => store.skillBanner )

    return (
        <section className="m-banner-slider">
            <Slider {...settings}>
                {
                    featuresList.map((feature) => {
                        return (
                            <div className="m-banner-slider__txt" key={Math.random()}>
                                <figure className="micon-round-arrow"></figure>
                                {/* <strong>26% Annual Growth</strong> for cloud related opportunities In IT Sector */}
                                { feature }
                            </div>
                        )
                    })
                }
            </Slider>
        </section>
    );
  }

export default BannerSlider;