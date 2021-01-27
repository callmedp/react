import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Swal from 'sweetalert2';
import { useForm } from "react-hook-form";
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { TextArea } from 'formHandler/mobileFormHandler/formFields';
import { fetchReviews } from 'store/DashboardPage/AddSubmitReview/actions/index';
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';

const RateProductModal = (props) => {
    const { setShowRateModal, idDict } = props
    const dispatch = useDispatch()
    const [showRatingModal, setShowRatingModal] = useState(false)
    const [showAllRatings, setShowAllRatings] = useState(true)
    const { register, handleSubmit, errors, reset } = useForm();

    const reviews = useSelector(store => store?.getReviews?.data);
    const { reviewLoader } = useSelector(store => store.loader);

    const submitReview = async values => {
        const new_review = {
            ...values,
            oi_pk: idDict?.orderId,
            rating: 5,
            type: 'POST'
        };

        dispatch(startReviewLoader());
        let addedReview = await new Promise((resolve, reject) => dispatch(fetchReviews({payload: new_review, resolve, reject })));
        dispatch(stopReviewLoader());
        reset(addedReview);
        Swal.fire({
            icon: 'success',
            text: 'Thanks for your valuable feedback !'
        })
        setShowRateModal(false)
    };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const handleEffects = async (values) => {
        const new_review = {
            ...values,
            prod: idDict?.prdId,
            type: 'GET'
        };
        try{
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startReviewLoader());
                await new Promise((resolve, reject) => dispatch(fetchReviews({payload: new_review, resolve, reject })));
                dispatch(stopReviewLoader());
            }
            else {
                delete window.config?.isServerRendered
            }
        }
        catch(e){
            dispatch(stopReviewLoader());
            Swal.fire({
                icon: 'error',
                text: 'Sorry! we are unable to fecth your data.'
            })
        }
    };

    useEffect(() => {
        handleEffects();
    }, [idDict])

    return (
        <>
            { reviewLoader && <Loader /> }
            <div className="m-slide-modal">
                {
                    showAllRatings &&
                    <div className="addcomments" style={{display: 'block'}}>
                        <span className="m-db-close" style={{ marginLeft: '13px' }} onClick={() => {setShowRateModal(false)}}>X</span>
                        
                        <div className="m-reviews-list">
                            <ul>
                                {
                                    reviews?.map((review, index) => {
                                        return(
                                            <li key={index}>
                                                <div className="card__rating">
                                                    <span className="rating">
                                                        { review?.rating?.map((star, index) => starRatings(star, index)) }
                                                        <span className="ml-5">{review?.average_rating?.toFixed(0)}/5</span>
                                                    </span>
                                                </div>

                                                <span className="m-reviews-list--date">{review?.created}</span>
                                                <p className="m-reviews-list--text">{review?.content}</p>
                                            </li>
                                        )
                                    })
                                }
                                {/* <li>
                                    <div className="card__rating">
                                        <span className="rating">
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <span> <strong>4</strong> /5</span>
                                        </span>
                                    </div>

                                    <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                    <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                                </li>
                                
                                <li>
                                    <div className="card__rating">
                                        <span className="rating">
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <span> <strong>4</strong> /5</span>
                                        </span>
                                    </div>

                                    <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                    <p className="m-reviews-list--text">Good Mentors with good experience</p>
                                </li>
                                <li>
                                    <div className="card__rating">
                                        <span className="rating">
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <span> <strong>4</strong> /5</span>
                                        </span>
                                    </div>

                                    <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                    <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                                </li>
                                
                                <li>
                                    <div className="card__rating">
                                        <span className="rating">
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <span> <strong>4</strong> /5</span>
                                        </span>
                                    </div>

                                    <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                    <p className="m-reviews-list--text">Good Mentors with good experience</p>
                                </li> */}
                            </ul>
                        </div>
                        
                        <div className="m-reviews-list-wrap--bottom">
                            <button className="btn btn-blue-outline px-30" onClick={() => {setShowAllRatings(false);setShowRatingModal(true)}}>Add new</button>
                        </div>
                    </div>
                }

                {
                    showRatingModal &&
                        <form onSubmit={handleSubmit(submitReview)}>
                            <div className="text-center">
                                <span className="m-db-close" onClick={() => {setShowRateModal(false)}}>X</span>
                                <h2>Add Review</h2>
                                <div className="m-enquire-now mt-15">
                                    <div className="m-form-group">
                                        <TextArea attributes={inboxForm.review} register={register} errors={!!errors ? errors[inboxForm.review.name] : ''} />
                                    </div>

                                    <button className="btn btn-blue" onClick={handleSubmit(submitReview)}>Submit</button>
                                </div>
                            </div>
                        </form>
                }

            </div>
        </>
    )
}

export default RateProductModal;