import React, {useState, useEffect} from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import './Reviews.scss';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProductReviews } from 'store/DetailPage/actions';
import ReviewModal from '../../../Common/Modals/reviewModal';
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { getCandidateId } from 'utils/storage.js';
import { siteDomain } from 'utils/domains';

const LearnersStories = (props) => {
    const {id, product_detail} = props;
    const [reviewModal, showReviewModal] = useState(false);
    const { reviewLoader } = useSelector(store => store.loader);
    const { prd_reviews : { prd_review_list, prd_rv_current_page, prd_rv_has_next, prd_rv_has_prev } } = useSelector( store => store.reviews );

    const dispatch = useDispatch();
    let currentPage = 1;

    useEffect( () => {
        handleEffects(currentPage);
    }, [id])

    const handleEffects = async (page) => {
        currentPage = page;

        try {
            dispatch(startReviewLoader())
            await new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: id, page: page, device: 'desktop' }, resolve, reject })));
            dispatch(stopReviewLoader())
        }
        catch (error) {
            dispatch(stopReviewLoader())
        }
        dispatch(stopReviewLoader());
    };

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="icon-fullstar" key={index}></em> :
                star === '+' ? <em className="icon-halfstar" key={index}></em> :
                    <em className="icon-blankstar" key={index}></em>
        )
    }

    const handleSelect = (selectedIndex, e) => {
        if(selectedIndex === 0 && e.target.className === 'carousel-control-next-icon' && prd_rv_has_next) handleEffects(prd_rv_current_page+1);
        if(selectedIndex === 0 && e.target.className === 'carousel-control-prev-icon' && prd_rv_has_prev) handleEffects(prd_rv_current_page-1);
    }

    const getReviews = (reviewData, idx) => {
        return (
            <Carousel.Item interval={1000000} key={idx}>
                <div className="d-flex col">
                    {
                        reviewData?.map((review, idx) => {
                            return ( 
                                <div className="col-sm-4" key={idx}>
                                    <div className="card">
                                        <span className="rating">
                                            {
                                                review?.rating?.map((star, index) => starRatings(star, index))
                                            }
                                        </span>
                                        <strong className="card__name">{review?.title}</strong>
                                        <p className="card__txt">{review?.content}</p>
                                        <strong>{ review?.user_name ? review?.user_name : 'Anonymous' }</strong>
                                        <span className="card__location">{review?.created}</span>
                                    </div>
                                </div>
                            )
                        })
                    }
                </div>
            </Carousel.Item>
        )
    }

    return (
        <>
        { reviewLoader ? <Loader /> : ''}
        <section id="reviews" className="container" data-aos="fade-up">
            {
                reviewModal ? <ReviewModal reviewModal={reviewModal} showReviewModal={showReviewModal} review={product_detail?.review} /> : ""
            }
            <div className="grid">
                <h2 className="heading2 m-auto pb-20">Reviews</h2>
                {
                    prd_review_list && prd_review_list.length > 0 ?
                    <Carousel className="reviews" onSelect={handleSelect}>
                        {
                            prd_review_list?.map(getReviews)
                        }
                    </Carousel>
                    : ""
                }

                <div className="d-flex mx-auto mt-20">
                    {
                        (product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={"#"} onClick={showReviewModal} className="btn btn-outline-primary btn-custom">Update your review</Link>
                        :
                        (!product_detail?.user_reviews && getCandidateId()) ?
                        <Link to={"#"} onClick={showReviewModal} className="btn btn-outline-primary btn-custom">Write a review</Link>
                        :
                        <Link to={"#"} onClick={() => window.location.href=`${siteDomain}/login/`} className="btn btn-outline-primary btn-custom">Write a review</Link>
                    }
                </div>
            </div>
        </section>
        </>
    )
}

export default LearnersStories;