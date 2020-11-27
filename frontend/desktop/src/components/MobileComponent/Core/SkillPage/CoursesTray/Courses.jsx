import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import './courses.scss';
import { useDispatch, useSelector } from 'react-redux';
import Product from './Product/product';

const Courses = (props) => {
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

    const { courseList } = useSelector(store => store.coursesTray)
    return (
    <section className="m-container mt-0 mb-0 pb-0">
        <h2 className="m-heading2 mb-10">Courses for you</h2>
        <div className="m-courses m-courses-slider ml-10n">
            <Slider {...settings}>
                {
                    courseList?.map((course, idx)=> <Product product={course} key={idx} compType='For You'/>)
                }
            </Slider>
        </div>

        <h2 className="m-heading2 mt-20 mb-20">More courses</h2>
        <div className="m-courses">
            {
                courseList?.map((course, idx)=> <Product product={course} key={idx + 100} compType='More Courses'/>)
            }
        </div>
    </section>
    );
  }

export default Courses;