import React, {useState} from 'react';
import { Modal } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
// import Swal from 'sweetalert2';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';
import { submitReview } from 'store/DashboardPage/AddSubmitReview/actions/index';
import { useForm } from "react-hook-form";
// import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
// import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../Common/Toast/toast'
import '../../SkillPage/NeedHelp/needHelp.scss';
import { imageUrl } from 'utils/domains';


const RateModal =(props) => {
    // const { handleClose, show, name, id } = props;
    const { showRateModal, setShowRateModal, oi_id, name } = props;

    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    let [rating, setRating] = useState(0);
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
        if(rating === 0){
            setShowError(true)
        }
        else{
            const new_review = {
                ...values,
                oi_pk: oi_id,
                rating: rating,
            };
    
            const response = await new Promise((resolve, reject) => dispatch(submitReview({payload: new_review, resolve, reject})));
    
            if(response) {
                if(!response?.error) setShowRateModal(false);
    
                Toast.fire({
                    type: response?.error ? 'error' : 'success',
                    title: response?.data.display_message ? response?.data.display_message : response.error
                });
            }
        }
    };

    return (
        <Modal show={showRateModal} onHide={setShowRateModal} className="db-modal db-page">
        <Modal.Header closeButton></Modal.Header>
        
        <Modal.Body>
            <div className="text-center db-rate-services need-help">
                <img src={`${imageUrl}/desktop/rate-services.png`} className="img-fluid" alt=""/>
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
                { showError && <p className="error_cls mt-10">* Please click on star for ratings</p> }
                <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                    <form onSubmit={handleSubmit(submitReviewFunc)}>
                            <InputField attributes={CoursesServicesForm.title} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.title.name] : false} />            

                            <TextArea attributes={CoursesServicesForm.review} register={register}
                                errors={!!errors ? errors[CoursesServicesForm.review.name] : ''} />
                        <br/>
                        <button className="btn btn-primary px-5" type="submit">Submit</button>
                    </form>
                </div>
            </Modal.Body>
        </Modal>
    )
}

export default RateModal;