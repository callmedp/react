import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import { submitReview } from 'store/DetailPage/actions';
import { useForm } from "react-hook-form";
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import Loader from '../Loader/loader';
import { Toast } from '../Toast/toast';
import { imageUrl } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';

const ReviewModal =(props) => {
    const { detReviewModal, showReviewModal, review, user_reviews, prdId } = props;
    const { reviewLoader } = useSelector(store => store.loader);
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    let [rating, setRating] = useState(review ? review?.average_rating : 0);
    let [clicked, setClicked] = useState(false);
    const [showError, setShowError] = useState(false)

    const fillNewStar = (star) => {
        if (star <= rating) return "icon-fullstar";
        else return "icon-blankstar";
    };

    const mouseOver = (e) => {
        setStars(4);
        setStars(e, "fullstar");
    };

    const mouseOut = (e) => (!clicked ? setStars(e) : null);

    const onClickEvent = (e, val = 0) => {
        setRating(
            parseInt(e.target.getAttribute("value"))
                ? parseInt(e.target.getAttribute("value"))
                : val
        );
        setStars(e, "fullstar");
        setClicked(true);
    };

    const setStars = (e, className = "blankstar") => {
        let data = typeof e == "number" ? e : parseInt(e.target.getAttribute("value")) - 1;
        let children = document.getElementsByClassName("rating-review")[0].children;
        for (let i = 0; i <= data; i++) {
            children[i].setAttribute("className", `icon-${className}`);
        }
    };

    // add new review
    const submitReviewFunc = async(values) => {
        if(user_reviews) MyGA.SendEvent('ln_review', 'ln_review', 'ln_submit_review', 'review_updated', '', false, true)
        else MyGA.SendEvent('ln_review', 'ln_review', 'ln_submit_review', 'review_written', '', false, true)

        if(rating === 0) return setShowError(true)
        else {
            dispatch(startReviewLoader())

            const new_review = {
                ...values,
                rating: rating ? rating : 5,
                product_id: prdId,
                update: review ? true : false
            };
    
            try {
                const response = await new Promise((resolve, reject) => dispatch(submitReview({payload: new_review, resolve, reject})));
        
                dispatch(stopReviewLoader())

                if(response) {
                    window.history.pushState({}, null, window.location.href.replace("?sm=true",''));

                    Toast.fire({
                        type: response?.error ? 'error' : 'success',
                        title: response?.error ? response?.message : response?.data?.message
                    });

                    showReviewModal(false);
                }
            }
            catch(error) {
                dispatch(stopReviewLoader())
                Toast.fire({
                    type: 'error',
                    title: error?.message
                });
            }
        }
    };

    let reviewedTitle = {
        className: "form-control",
        type: "text",
        name: "title",
        id: "title",
        placeholder: " ",
        label: "Title",
        defaultValue: review?.title,
        inputType: 'input',
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
    };

    let reviewedContent = {
        className: "form-control",
        type: "text",
        name: "review",
        id: "review",
        placeholder: " ",
        label: "Review",
        defaultValue: review?.content,
        inputType: 'input',
        rows: 3,
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
    };

    return (
        <>
        { reviewLoader ? <Loader /> : ''}
        <Modal show={detReviewModal} onHide={showReviewModal} onClick={() => {return window.history.pushState({}, null, window.location.href.replace("?sm=true",''))}} className="db-modal db-page">
        <Modal.Header closeButton></Modal.Header>
        
        <Modal.Body>
            <div className="text-center db-rate-services need-help">
                <img src={`${imageUrl}desktop/rate-services.png`} className="img-fluid" alt=""/>
                <p className="db-rate-services--heading">Rate Course</p>
                
                <span className="rating-review">
                    {[1, 2, 3, 4, 5].map((value,indx) => {
                        return (
                            <i
                            key={indx}
                            value={value}
                            className={fillNewStar(value)}
                            onMouseOver={(e) => mouseOver(e)}
                            onMouseOut={(e) => mouseOut(e)}
                            onClick={(e) => onClickEvent(e)}
                            ></i>
                        );
                    })} 
                </span>
                { showError && <p className="error_cls mt-10">* Please click on star for ratings</p> }
                <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                {/* {errors}  */}
                {/* {errors[CoursesServicesForm.review.name]} */}
                    <form onSubmit={handleSubmit(submitReviewFunc)}>
                            <InputField attributes={review ? reviewedTitle : CoursesServicesForm.title} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.title.name] : false} />            

                            <TextArea attributes={review ? reviewedContent : CoursesServicesForm.review} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.review.name] : ""} />
                        <br/>
                        <button className="btn btn-primary px-5" type="submit">{review ? 'Update' : 'Submit'}</button>
                    </form>
                </div>
            </Modal.Body>
        </Modal>
        </>
    )
}

export default ReviewModal;