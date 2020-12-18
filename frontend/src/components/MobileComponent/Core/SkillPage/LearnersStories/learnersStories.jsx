import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './learnersStories.scss';
import { useSelector } from 'react-redux';

const LearnersStories = (props) => {
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
    const { testimonialCategory } = useSelector(store => store.skillBanner)

    const getStories = (item, index) => {
        return (
            <div className="m-card text-center" key={index.toString() + item.userName}>
                <span className="m-card__name">{item.firstName ? item.firstName[0].toUpperCase() : ""}{item.lastName ? item.lastName[0].toUpperCase() : ""}</span>
                <p className="m-card__txt">{item.review}</p>
                <strong>{item.firstName + item.lastName}</strong>
                <span className="m-card__location">{item.company ? item.company : <br />}</span>
            </div>
        )
    }
    
    return (
        testimonialCategory.length ? (
            <section className="m-container mt-0 mb-0 pb-0">
                <h2 className="m-heading2 mb-10">Learners stories</h2>
                <div className="m-learner-stories ml-10n">
                    <Slider {...settings}>
                        { testimonialCategory?.map(getStories) }
                    </Slider>
                </div>
            </section>):null
    );
  }

export default LearnersStories;