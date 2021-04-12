import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from 'react-redux';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import {Link} from 'react-router-dom';
import './reviews.scss';
import { fetchProductReviews } from 'store/DetailPage/actions';

const Reviews = (props) => {
    const { showReviewModal, prdId } = props
    const { prd_review_list, prd_rv_total } = useSelector( store => store.reviews )
    const [pageId, updatePageId] = useState(2)
    const dispatch = useDispatch()

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
        afterChange: function(index) {
            if ((index % 7 === 0 && pageId < index ) && pageId <= prd_rv_total) {
                new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: prdId?.split('-')[1], page: pageId, device: 'mobile'}, resolve, reject })));
                updatePageId(pageId + 1);
            }
        }
    }

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" id="review" data-aos="fade-up">
            <div className="d-flex" itemProp="review" itemScope itemtype="https://schema.org/Review">
                <h2 className="m-heading2 mb-10">Review</h2>
                <Link to={'#'} className="ml-auto fs-13 font-weight-bold" onClick={() => showReviewModal(true) }>Write a review</Link>
            </div>
            <div className="m-reviews">
                <Slider {...settings}>
                    {
                        prd_review_list?.map((review, idx) => {
                            return (
                                <div className="m-card" key={idx}>
                                    <span className="m-rating" itemProp="ratingValue">
                                    {
                                        review?.rating?.map((star, index) => starRatings(star, index))
                                    }
                                    </span>
                                    <strong className="m-card__name" itemProp="name">{review?.title}</strong>
                                    <p className="m-card__txt" itemProp="reviewBody">{review?.content}</p>
                                    <strong itemProp="author">By { review?.user_name ? review?.user_name : "Anonymous" }</strong>
                                    <span className="m-card__location" itemProp="datePublished">{review?.created}</span>
                                </div>
                            )
                        })
                    }
                </Slider>
            </div>
        </section>
    );
  }

export default Reviews;