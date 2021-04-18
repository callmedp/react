import React, {useState, useEffect} from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import './Reviews.scss';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProductReviews } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';
import { getCandidateId } from 'utils/storage.js';
import { siteDomain } from 'utils/domains';

const Reviews = (props) => {
    const {id, product_detail, pUrl, showReviewModal} = props;
    const { reviewLoader } = useSelector(store => store.loader);
    const [carIndex, setIndex] = useState(0);
    const dispatch = useDispatch();
    const { prd_review_list, prd_rv_current_page, prd_rv_has_next } = useSelector( store => store.reviews );

    let currentPage = 1;

    useEffect( () => {
        handleEffects(currentPage)
    },[id])

    const handleEffects = async (page) => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: id, page: page, device: 'desktop' }, resolve, reject })));
        }
        catch (error) {
            console.log('error in reviews api');
        }
    };

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="icon-fullstar" key={index}></em> :
                star === '+' ? <em className="icon-halfstar" key={index}></em> :
                    <em className="icon-blankstar" key={index}></em>
        )
    }

    const handleSelect = (selectedIndex, e) => {
        if (e !== undefined) {
            setIndex(selectedIndex);
            if((selectedIndex % 2 === 0) && e.target.className === 'carousel-control-next-icon' && prd_rv_has_next) {
                handleEffects(prd_rv_current_page+1);
            }
        }
    }

    return (
        <>
            { reviewLoader ? <Loader /> : ''}
            <section id="reviews" className="container" data-aos="fade-up">
                <div className="grid">
                    <h2 className="heading2 text-center pb-20">Reviews</h2>
                </div>

                {
                    (prd_review_list && prd_review_list?.length > 0) &&
                    <Carousel className="reviews" activeIndex={carIndex} onSelect={handleSelect} >
                        {
                            prd_review_list?.map((reviewData, idx) => {
                                return (
                                    <Carousel.Item interval={10000000000} key={idx}>
                                        <div className="d-flex col">
                                            {
                                                reviewData?.map((review, indx) => {
                                                    return (
                                                        <div className="col-sm-4" key={indx} itemProp="review" itemScope itemType="https://schema.org/Review">
                                                            <div className="card">
                                                                <span className="rating" itemProp="ratingValue">
                                                                    {
                                                                        review?.rating?.map((star, index) => starRatings(star, index))
                                                                    }
                                                                </span>
                                                                <strong className="card__name" itemProp="name">{review?.title ? review?.title : '  '}</strong>
                                                                <p className="card__txt" itemProp="reviewBody">{review?.content}</p>
                                                                <strong itemProp="author">{ review?.user_name ? review?.user_name : 'Anonymous' }</strong>
                                                                <span className="card__location" itemProp="datePublished">{review?.created ? review?.created : '  '}</span>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            }
                                        </div>
                                    </Carousel.Item>
                                )
                            })
                        }
                    </Carousel>
                }

                <div className="d-flex mx-auto mt-20">
                    {
                        (product_detail?.user_reviews && getCandidateId()) ?
                            <Link to={"#"} onClick={showReviewModal} className="btn btn-outline-primary btn-custom mx-auto">Update your review</Link>
                        :
                        (!product_detail?.user_reviews && getCandidateId()) ?
                            <Link to={"#"} onClick={showReviewModal} className="btn btn-outline-primary btn-custom mx-auto">Write a review</Link>
                        : 
                        <a href={`${siteDomain}/login/?next=${pUrl}?sm=true`} className="btn btn-outline-primary btn-custom mx-auto">Write a review</a>
                    }
                </div>
            </section>
        </>
    )
}

export default Reviews;