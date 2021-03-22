import React, { useEffect } from "react";
import { useSelector, useDispatch } from 'react-redux';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import {Link} from 'react-router-dom';
import './reviews.scss';

const Reviews = (props) => {
    const { showReviewModal } = props
    const { prd_reviews : { prd_review_list } } = useSelector( store => store.reviews )

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

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <h2 className="m-heading2 mb-10">Review</h2>
                <Link className="ml-auto fs-13 font-weight-bold" onClick={() => showReviewModal(true) }>Write a review</Link>
            </div>
            <div className="m-reviews">
                <Slider {...settings}>
                    {
                        prd_review_list?.map((review, idx) => {
                            return (
                                <div className="m-card" key={idx}>
                                    <span className="m-rating">
                                    {
                                        review?.rating?.map((star, index) => starRatings(star, index))
                                    }
                                    </span>
                                    <strong className="m-card__name">{review?.title}</strong>
                                    <p className="m-card__txt">{review?.content}</p>
                                    <strong>By { review?.user_name ? review?.user_name : "Anonymous" }</strong>
                                    <span className="m-card__location">{review?.created}</span>
                                </div>
                            )
                        })
                    }
                    
                    {/* <div className="m-card">
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
                    </div> */}
                </Slider>
            </div>
        </section>
    );
  }

export default Reviews;