import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import './courses.scss';
import { useDispatch, useSelector } from 'react-redux';
import Product from './Product/product';

const Assessment = (props) => {
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

    const { assessmentList } = useSelector(store => store.coursesTray)
    return (
    <section className="m-container mt-0 mb-0 pb-0">
        <h2 className="m-heading2 mb-10">Assessment for you</h2>
        <div className="m-courses m-courses-slider ml-10n">
            <Slider {...settings}>
                {
                    assessmentList?.map((assessment, idx)=> <Product product={assessment} key={idx} compType='For You'/>)
                }
            </Slider>
        </div>

        <h2 className="m-heading2 mt-20 mb-20">More assessment</h2>
        <div className="m-courses">
            {
                assessmentList?.map((assessment, idx)=> <Product product={assessment} key={idx + 100} compType='More Courses'/>)
            }
            
        </div>
    </section>
    );
  }

export default Assessment;