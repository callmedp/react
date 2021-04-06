import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import { submitReview } from 'store/DetailPage/actions';
import { useForm } from "react-hook-form";
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import Loader from '../Loader/loader';
import { Toast } from '../Toast/toast'
import { imageUrl } from 'utils/domains';

const ReviewModal =(props) => {
    const { reviewModal, showReviewModal, review } = props;
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
            children[i].setAttribute("class", `icon-${className}`);
        }
    };

    // add new review
    const submitReviewFunc = async(values) => {
        dispatch(startReviewLoader())
        if(rating === 0){
            setShowError(true)
        }
        else {
            const new_review = {
                ...values,
                rating: rating ? rating : 5,
            };
    
            const response = await new Promise((resolve, reject) => dispatch(submitReview({payload: new_review, resolve, reject})));
    
            dispatch(stopReviewLoader())

            if(response) {
                if(!response?.error) showReviewModal(false);
    
                Toast.fire({
                    type: response?.error ? 'error' : 'success',
                    title: response?.data?.display_message ? response?.data?.display_message : response?.display_message
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
        value: review?.title,
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
        label: "Type Here",
        value: review?.content,
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
        <Modal show={reviewModal} onHide={showReviewModal} className="db-modal db-page">
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
                    <form onSubmit={handleSubmit(submitReviewFunc)}>
                            <InputField attributes={review ? reviewedTitle : CoursesServicesForm.title} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.title.name] : false} />            

                            <TextArea attributes={review ? reviewedContent : CoursesServicesForm.review} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.review.name] : ''} />
                        <br/>
                        <button className="btn btn-primary px-5" type="submit">Submit</button>
                    </form>
                </div>
            </Modal.Body>
        </Modal>
        </>
    )
}

export default ReviewModal;