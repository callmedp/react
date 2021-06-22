import React, { useState, useRef } from "react";
import { useDispatch } from 'react-redux';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import {Link} from 'react-router-dom';
import './reviews.scss';
import { fetchProductReviews } from 'store/DetailPage/actions';
import { getCandidateId } from 'utils/storage.js';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const Reviews = (props) => {
    const { showReviewModal, prdId, product_detail, pUrl, prd_review_list, prd_rv_total } = props;
    const [pageId, updatePageId] = useState(2);
    const dispatch = useDispatch();
    const sendLearningTracking = useLearningTracking();
    const sliderRef = useRef();

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
            console.log(pageId, index, prd_rv_total)
            if ((index % 7 === 0 && pageId < index ) && pageId <= prd_rv_total) {
                try {
                    new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: prdId?.split('-')[1], page: pageId, device: 'mobile'}, resolve, reject })));
                    updatePageId(pageId + 1);
                }
                catch(error) {}
            }

            sendLearningTracking({
                productId: '',
                event: `course_detail_${stringReplace(product_detail?.prd_H1)}_reviews_next_previous_${index}_clicked`,
                pageTitle:`course_detail`,
                sectionPlacement:'reviews',
                eventCategory: ``,
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: index,
            })
        }
    }

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const writeReviewTracking = (name, logged) => {
        if(logged) showReviewModal(state => !state);
        
        sendLearningTracking({
            productId: '',
            event: `course_detail_${name}_clicked`,
            pageTitle:`course_detail`,
            sectionPlacement:'reviews',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section className="m-container mt-0 mb-0 pb-0" id="reviews" data-aos="fade-up">
            <div className="d-flex">
                <h2 className="m-heading2 mb-10">Review</h2>
                {
                    (product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={'#'} className="ml-auto fs-13 font-weight-bold" onClick={() => writeReviewTracking('update_your_review', true)}>Update your review</Link>
                    :
                    (!product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={'#'} className="ml-auto fs-13 font-weight-bold" onClick={() => writeReviewTracking('write_a_review', true)}>Write a review</Link>
                    : 
                    <a href={`${siteDomain}/login/?next=${pUrl}?sm=true`} onClick={() => writeReviewTracking('write_a_review_non_logged_in', false)} className="ml-auto fs-13 font-weight-bold" >Write a review</a>
                }
                
            </div>
            {
                prd_review_list && prd_review_list?.length > 0 &&
                <div className="m-reviews">
                    <Slider {...settings} ref={sliderRef}>
                        {
                            prd_review_list?.map((review, idx) => {
                                return (
                                    <div className="m-card" key={idx} itemProp="review" itemScope itemType="https://schema.org/Review">
                                        <span className="m-rating" itemProp="reviewRating" itemScope itemType="http://schema.org/Rating">
                                            <span itemProp="ratingValue">
                                                {
                                                    review?.rating?.map((star, index) => starRatings(star, index))
                                                }
                                            </span>
                                        </span>
                                        <strong className="m-card__name" itemProp="name" content={review?.title || ""}>{review?.title ? review?.title : <>&nbsp;</>}</strong>
                                        <p className="m-card__txt" itemProp="description">{review?.content}</p>
                                        <strong itemProp="author" itemType="http://schema.org/Person" itemScope>
                                            <span itemProp="name" content={review?.user_name ? review?.user_name : "Anonymous"}>By { review?.user_name ? review?.user_name : "Anonymous" }</span>
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