import React, { useEffect, useState } from 'react';
// import { useDispatch, useSelector } from 'react-redux';
// import Swal from 'sweetalert2';
// import { useForm } from "react-hook-form";
// import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
// import { TextArea, InputField } from 'formHandler/mobileFormHandler/formFields';
// import { fetchReviews, submitReview } from 'store/DashboardPage/AddSubmitReview/actions/index';
// import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
// import Loader from '../../../Common/Loader/loader';
import './rating.scss';

const RateProductModal = (props) => {
    const { setShowRateModal, setShowRatingsModal, oi_id, idDict, reviewData } = props
    // const dispatch = useDispatch()
    // const [showRatingModal, setShowRatingModal] = useState(false)
    // const [showAllRatings, setShowAllRatings] = useState(true)
    // const [inputStar, setInputStar] = useState(5);
    // const { register, handleSubmit, errors, reset } = useForm();

    // const reviewList = useSelector( store => store?.getReviews?.data );
    // const { reviewLoader } = useSelector(store => store.loader);

    // const submitReviews = async values => {
    //     const new_review = {
    //         ...values,
    //         oi_pk: oi_id ? oi_id : idDict?.orderId,
    //         rating: inputStar ? inputStar : 5,
    //         type: 'POST'
    //     };

    //     dispatch(startReviewLoader());
    //     let addedReview = await new Promise((resolve, reject) => dispatch(submitReview({ payload: new_review, resolve, reject })));
    //     dispatch(stopReviewLoader());

    //     if(addedReview) {
    //         if(!addedReview?.error) setShowRateModal(false);

    //         Swal.fire({
    //             icon: addedReview?.error ? 'error' : 'success',
    //             text: addedReview.display_message ? addedReview.display_message : addedReview.error
    //         });
    //     }
        
    //     reset(addedReview);
    //     setShowRateModal(false)
    // };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    // const handleEffects = async (values) => {
    //     const new_review = {
    //         ...values,
    //         prod: oi_id ? oi_id : idDict?.prdId,
    //         type: 'GET'
    //     };
    //     try{
    //         dispatch(startReviewLoader());
    //         await new Promise((resolve, reject) => dispatch(fetchReviews({ payload: new_review, resolve, reject })));
    //         dispatch(stopReviewLoader());
    //     }
    //     catch(e){
    //         dispatch(stopReviewLoader());
    //         Swal.fire({
    //             icon: 'error',
    //             text: 'Sorry! we are unable to fecth your data.'
    //         })
    //     }
    // };

    // useEffect(() => {
    //     handleEffects();
    // }, [oi_id ? oi_id : idDict])

    return (
        <>
            {/* { reviewLoader && <Loader /> } */}
            <div className="m-slide-modal">
                {/* {
                    showAllRatings && */}
                    <div className="addcomments" style={{display: 'block'}}>
                        <span className="m-db-close" style={{ marginLeft: '13px' }} onClick={() => {setShowRatingsModal(false)}}>&#x2715;</span>
                        {/* {
                            reviewList?.length > 0 ?  */}
                                <div className="m-reviews-list">
                                    <ul>
                                        {
                                            reviewData?.map((review, index) => {
                                                return(
                                                    <li key={index}>
                                                        <div className="card__rating">
                                                            <span className="rating">
                                                                { review?.rating?.map((star, index) => starRatings(star, index)) }
                                                                <span className="ml-5">{review?.average_rating?.toFixed(0)}/5</span>
                                                            </span>
                                                        </div>

                                                        <span className="m-reviews-list--date">{review?.title ? review?.title + ' - ' : ""}{review?.created}</span>
                                                        <p className="m-reviews-list--text">{review?.content ? review?.content : ''}</p>
                                                    </li>
                                                )
                                            })
                                        }
                                    </ul>
                                </div>  
                                {/* :
                                <p className="text-center px-30 py-30">No rating yet, please review it by clicking add new button</p>
                        } */}
                        <div className="m-reviews-list-wrap--bottom">
                            <button className="btn btn-blue-outline px-30" onClick={() => {setShowRatingsModal(false);setShowRateModal(true)}}>Add new</button>
                        </div>
                    </div>
                {/* } */}

                {/* {
                    // showRatingModal &&
                    showAllRatings &&
                        <form onSubmit={handleSubmit(submitReviews)}>
                            <div className="text-center">
                                <span className="m-db-close" onClick={() => {setShowRateModal(false)}}>&#x2715;</span>
                                <h2>Write a Review</h2>

                                <span className="m-rating m-rate-review">
                                {
                                    [1, 2, 3, 4, 5].map((value,indx) => {
                                        return (
                                            <em
                                            key={indx}
                                            value={value}
                                            className={value <= inputStar? "micon-fullstar ml-5" : "micon-blankstar ml-5"}
                                            onClick={() => setInputStar(value)} />
                                        );
                                })}
                                </span>
                                <p>Tap on rate to scale of 1-5</p>
                                <div className="m-enquire-now mt-15">
                                    <InputField attributes={inboxForm.title} register={register} customClass='m-form-group mb-0' errors={!!errors ? errors[inboxForm.title.name] : false} />  
                                    
                                    <TextArea attributes={inboxForm.review} register={register} errors={!!errors ? errors[inboxForm.review.name] : ''} />

                                    <button className="btn btn-blue" onClick={handleSubmit(submitReviews)}>Submit</button>
                                </div>
                            </div>
                        </form>
                } */}

            </div>
        </>
    )
}

export default RateProductModal;