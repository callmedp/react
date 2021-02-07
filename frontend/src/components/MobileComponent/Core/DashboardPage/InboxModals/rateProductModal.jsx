import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
// import Swal from 'sweetalert2';
import { useForm } from "react-hook-form";
import inboxForm from 'formHandler/mobileFormHandler/formData/inboxForm';
import { TextArea, InputField } from 'formHandler/mobileFormHandler/formFields';
import { fetchReviews, submitReview } from 'store/DashboardPage/AddSubmitReview/actions/index';
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import './rating.scss';
import { showSwal } from 'utils/swal'

const RateProductModal = (props) => {
    const { setShowRateModal, oi_id, idDict } = props
    const dispatch = useDispatch()
    // const [showRatingModal, setShowRatingModal] = useState(false)
    // const [showAllRatings, setShowAllRatings] = useState(true)
    const [inputStar, setInputStar] = useState(0);
    const { register, handleSubmit, errors, reset } = useForm();
    const [showError, setShowError] = useState(false)

    // const reviewList = useSelector( store => store?.getReviews?.data );
    const { reviewLoader } = useSelector(store => store.loader);

    const submitReviews = async values => {
        if(inputStar === 0){
            setShowError(true)
        }
        else{
            const new_review = {
                ...values,
                oi_pk: oi_id ? oi_id : idDict?.orderId,
                rating: inputStar ? inputStar : 5,
                type: 'POST'
            };

            dispatch(startReviewLoader());
            let addedReview = await new Promise((resolve, reject) => dispatch(submitReview({ payload: new_review, resolve, reject })));
            dispatch(stopReviewLoader());

            if(addedReview) {
                if(!addedReview?.error) setShowRateModal(false);

                showSwal((addedReview?.error ? 'error' : 'success'), (addedReview?.data?.display_message ? addedReview?.data?.display_message : addedReview.error))
            }
            
            reset(addedReview);
            setShowRateModal(false)
        }
    };


    return (
        <>
            { reviewLoader && <Loader /> }
            <div className="m-slide-modal">
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
                                { showError && <p className="error_cls">* Please click on star for ratings</p> }
                                <p>Click on rate to scale of 1-5</p>
                                <div className="mdb-enquire-now mt-15">
                                    <InputField attributes={inboxForm.title} register={register} customClass='m-form-group' errors={!!errors ? errors[inboxForm.title.name] : false} />  
                                    
                                    <TextArea attributes={inboxForm.review} register={register} errors={!!errors ? errors[inboxForm.review.name] : ''} />

                                    <button className="btn btn-blue" onClick={handleSubmit(submitReviews)}>Submit</button>
                                </div>
                            </div>
                        </form>

            </div>
        </>
    )
}

export default RateProductModal;