import React, { Component } from "react";
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './ourVendors.scss';
import { useSelector } from 'react-redux';

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
    const { vendorList } = useSelector(store => store.allCategories);

    return (
        <section className="m-container" data-aos="fade-up">
            <h2 className="m-heading2 text-center mx-auto">Our Vendors</h2>
            <div className="m-our-vendors-slider">
                <Slider {...settings}>
                    {
                        vendorList?.map((vendor) =>{
                            return (
                                <div className="m-our-vendors-slider__txt" key={vendor.pk}>
                                    <figure>
                                        <img src={vendor.image} className="img-fluid" alt={vendor.name} />
                                    </figure>
                                </div>
                            )
                        })
                    }
                </Slider>
            </div>
        </section>
    )
}
   
export default OurVendors;