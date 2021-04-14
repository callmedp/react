import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import './modals.scss'
import DetailForm from 'formHandler/mobileFormHandler/formData/detailPageForm';
import { TextArea, InputField } from 'formHandler/mobileFormHandler/formFields';
import { useForm } from "react-hook-form";
import { submitReview } from 'store/DetailPage/actions';
import { showSwal } from 'utils/swal'
 
const ReviewModal = (props) => {
    const { showReviewModal, prdId, review } = props
    const [inputStar, setInputStar] = useState(review ? review?.average_rating : 0);
    const { register, handleSubmit, errors, reset } = useForm();
    const [showError, setShowError] = useState(false)
    const dispatch = useDispatch()

    const submitReviews = async values => {
        if(inputStar === 0){
            setShowError(true)
        }
        else{
            const review_values = {
                ...values,
                rating: inputStar ? inputStar : 5,
                product_id: prdId?.split('-')[1]
            }

            try{
                let addedReview = await new Promise((resolve, reject) => dispatch(submitReview({ payload: review_values, resolve, reject })));

                if(addedReview) {
                    if(!addedReview?.error) showReviewModal(false);

                    showSwal((addedReview?.error ? 'error' : 'success'), (addedReview?.data?.message ? addedReview?.data?.message : addedReview.error))
                }
                
                reset(addedReview);
                showReviewModal(false)
            }
            catch{
                showSwal('error', 'Something went wrong!')
            }
            
        }
    }

    const getTitlewithReview = () => {
        return {
            ... DetailForm.title,
            'defaultValue' : review?.title ? review?.title : ''
        }
    }

    const getContentwithReview = () => {
        return {
            ... DetailForm.review,
            'defaultValue' : review?.content ? review?.content : ''
        }
    }

    return(
        <div className="m-container m-enquire-now m-review-modal m-form-pos-center" data-aos="zoom-in">
            <div className="m-modal-body">
                {/* <Link to={"#"} className="m-close" onClick={() => showReviewModal(false)}>x</Link> */}
                <span className="m-close" onClick={() => showReviewModal(false)}>x</span>
                <h2 className="m-heading2 text-center">Write a Review</h2>
                <span className="m-rating m-big-review-star">
                    {
                        [1, 2, 3, 4, 5].map((value,indx) => {
                            return (
                                <em
                                key={indx}
                                value={value}
                                className={value <= inputStar? "micon-fullstar" : "micon-blankstar"}
                                onClick={() => setInputStar(value)} />
                            );
                    })}
                </span> 
                { showError && <p className="error_cls">* Please click on star for ratings</p> }
                <span>Click on rate to scale of 1-5</span>
                <form className="mt-20" onSubmit={handleSubmit(submitReviews)}>
                    {/* <div className="m-form-group m-error">
                        <input className="m-input_field" type="text" name="name" id="name" placeholder=" " />
                        <label className="m-input_label" htmlFor="name">Title*</label>
                    </div>
                    <div className="m-form-group">
                        <textarea type="text" className="input_field" name="review" id="review" placeholder=" " />
                        <label className="m-input_label" htmlFor="review">Review*</label>
                    </div> */}
                    <InputField attributes={getTitlewithReview()} register={register} customClass='m-form-group' review={review} errors={!!errors ? errors[DetailForm.title.name] : false} />  
                                    
                    <TextArea attributes={getContentwithReview()} register={register} review={review} errors={!!errors ? errors[DetailForm.review.name] : ''} />
                    <div className="m-form-group">
                        <button className="btn-blue">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default ReviewModal;