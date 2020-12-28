import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './ourVendors.scss';

const OurVendors = (props) => {
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
        <section className="m-container" data-aos="fade-up">
            <h2 className="m-heading2 text-center mx-auto">Our Vendors</h2>
            <div className="m-our-vendors-slider">
                <Slider {...settings}>
                    <div className="m-our-vendors-slider__txt">
                        <figure>
                            <img src="./media/images/mobile/shine-learning-vendor.png" className="img-fluid" alt="Shine Learning" />
                        </figure>
                    </div>
                    <div className="m-our-vendors-slider__txt">
                        <figure>
                            <img src="./media/images/mobile/361minds-vendor.png" className="img-fluid" alt="Shine Learning" />
                        </figure>
                    </div>
                    <div className="m-our-vendors-slider__txt">
                        <figure>
                            <img src="./media/images/mobile/vskills-vendor.png" className="img-fluid" alt="Shine Learning" />
                        </figure>
                    </div>
                    <div className="m-our-vendors-slider__txt">
                        <figure>
                            <img src="./media/images/mobile/skillsoft-vendor.png" className="img-fluid" alt="Shine Learning" />
                        </figure>
                    </div>
                    <div className="m-our-vendors-slider__txt">
                        <figure>
                            <img src="./media/images/mobile/edurekha-vendor.png" className="img-fluid" alt="Shine Learning" />
                        </figure>
                    </div>
                </Slider>
            </div>
        </section>
    )
}
   
export default OurVendors;