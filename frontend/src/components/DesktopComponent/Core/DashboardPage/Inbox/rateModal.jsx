import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import { submitReview } from 'store/DashboardPage/AddSubmitReview/actions/index';
import { useForm } from "react-hook-form";
import { useDispatch } from 'react-redux';
import {Toast} from '../../../Common/Toast/toast';

const RateModal =(props) => {
    const { handleClose, show, name, id } = props;
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    let [rating, setRating] = useState(5);
    let [clicked, setClicked] = useState(false);

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
        const new_review = {
            ...values,
            oi_pk: id,
            rating: rating,
            full_name: localStorage.getItem('first_name') || '' + ' ' + localStorage.getItem('last_name') || ''
            // full_name: 'Priya kharb'
        };

        const response = await new Promise((resolve, reject) => dispatch(submitReview({new_review, resolve, reject})));

        if(response) {
            handleClose(false);
            Toast.fire({
                type: 'success',
                title: response.display_message
            });
        }
    };

    return (
        <Modal show={show} onHide={handleClose} className="db-modal">
        <Modal.Header closeButton></Modal.Header>
        
        <Modal.Body>
            <div className="text-center db-rate-services need-help">
                <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                <p className="db-rate-services--heading">Rate {name}</p>
                
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
                <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                    <form onSubmit={handleSubmit(submitReviewFunc)}>
                        <div className="form-group error">
                            <InputField attributes={CoursesServicesForm.title} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.title.name] : ''} />
                            <label htmlFor="">Title</label>
                        </div>

                        <div className="form-group">
                            <TextArea attributes={CoursesServicesForm.review} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.review.name] : ''} />
                        </div>

                        <button className="btn btn-primary px-5" type="submit">Submit</button>
                    </form>
                </div>
            </Modal.Body>
        </Modal>
    )
}

export default RateModal;