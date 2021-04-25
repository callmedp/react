import React, { useState } from "react";
import { useSelector, useDispatch } from 'react-redux';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import {Link} from 'react-router-dom';
import './reviews.scss';
import { fetchProductReviews } from 'store/DetailPage/actions';
import { getCandidateId } from 'utils/storage.js';
import { siteDomain } from 'utils/domains';

const Reviews = (props) => {
    const { showReviewModal, prdId, product_detail, pUrl, prd_review_list, prd_rv_total } = props;
    const [pageId, updatePageId] = useState(2);
    const dispatch = useDispatch();

    const settings = {
        dots: false,
        arrows: true,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        // variableWidth: true,
        afterChange: function(index) {
            if ((index % 7 === 0 && pageId < index ) && pageId <= prd_rv_total) {
                try {
                    new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: prdId?.split('-')[1], page: pageId, device: 'mobile'}, resolve, reject })));
                    updatePageId(pageId + 1);
                }
                catch(error) {}
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
        <section className="m-container mt-0 mb-0 pb-0" id="reviews" data-aos="fade-up">
            <div className="d-flex">
                <h2 className="m-heading2 mb-10">Review</h2>
                {
                    (product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={'#'} className="ml-auto fs-13 font-weight-bold" onClick={() => showReviewModal(true) }>Update your review</Link>
                    :
                    (!product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={'#'} className="ml-auto fs-13 font-weight-bold" onClick={() => showReviewModal(true) }>Write a review</Link>
                    : 
                    <a href={`${siteDomain}/login/?next=${pUrl}?sm=true`} className="ml-auto fs-13 font-weight-bold" >Write a review</a>
                }
                
            </div>
            {
                prd_review_list && prd_review_list?.length > 0 &&
                <div className="m-reviews">
                    <Slider {...settings}>
                        {
                            prd_review_list?.map((review, idx) => {
                                return (
                                    <div className="m-card" key={idx} itemProp="review" itemScope itemType="https://schema.org/Review">
                                        <span className="m-rating" itemProp="reviewRating" itemScope itemType="http://schema.org/Rating" itemProp="ratingValue">
                                            <span itemProp="ratingValue">
                                                {
                                                    review?.rating?.map((star, index) => starRatings(star, index))
                                                }
                                            </span>
                                        </span>
                                        <strong className="m-card__name" itemProp="name">{review?.title ? review?.title : <>&nbsp;</>}</strong>
                                        <p className="m-card__txt" itemProp="description">{review?.content}</p>
                                        <strong itemProp="author" itemType="http://schema.org/Person" itemScope>
                                            <span itemProp="name">By { review?.user_name ? review?.user_name : "Anonymous" }</span>
                                        </strong>
                                        <span className="m-card__location" itemProp="datePublished">{review?.created ? review?.created : <>&nbsp;</>}</span>
                                    </div>
                                )
                            })
                        }
                    </Slider>
                </div>
            }
        </section>
    );
}

export default Reviews;