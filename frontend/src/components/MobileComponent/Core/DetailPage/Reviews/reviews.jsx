import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import {Link} from 'react-router-dom';
import './reviews.scss';

const Reviews = (props) => {
    const { showReviewModal } = props

    const settings = {
        dots: false,
        arrows: true,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        arrows: false,
        // variableWidth: true,
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <h2 className="m-heading2 mb-10">Review</h2>
                <Link className="ml-auto fs-13 font-weight-bold" onClick={() => showReviewModal(true) }>Write a review</Link>
            </div>
            <div className="m-reviews">
                <Slider {...settings}>
                    <div className="m-card">
                        <span className="m-rating">
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-blankstar"></em>
                        </span>
                        <strong className="m-card__name">Great service</strong>
                        <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                        <strong>By Abhishek Sinha</strong>
                        <span className="m-card__location">Dec 1, 2019</span>
                    </div>
                    <div className="m-card">
                        <span className="m-rating">
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-blankstar"></em>
                        </span>
                        <strong className="m-card__name">Great service</strong>
                        <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                        <strong>By Gaurav Singh</strong>
                        <span className="m-card__location">Dec 1, 2019</span>
                    </div>
                    <div className="m-card">
                        <span className="m-rating">
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-blankstar"></em>
                        </span>
                        <strong className="m-card__name">Great service</strong>
                        <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                        <strong>By Manish Sharma</strong>
                        <span className="m-card__location">Dec 1, 2019</span>
                    </div>
                </Slider>
            </div>
        </section>
    );
  }

export default Reviews;