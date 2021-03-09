import React from 'react';
import {Link} from 'react-router-dom';
import Modal from 'react-modal';
import './modals.scss'
 
const ReviewModal = (props) => {
    return(
        <div class="m-container m-enquire-now m-review-modal m-form-pos-center" data-aos="zoom-in">
            <div className="m-modal-body">
                <Link to={"#"} className="m-close">x</Link>
                <span className="m-close">x</span>
                <h2 className="m-heading2 text-center">Write a Review</h2>
                <span className="m-rating">
                    <em className="micon-fullstar-big"></em>
                    <em className="micon-fullstar-big"></em>
                    <em className="micon-fullstar-big"></em>
                    <em className="micon-fullstar-big"></em>
                    <em className="micon-blankstar-big"></em>
                    <span>Click on rate to scale of 1-5</span>
                </span>
                <form className="mt-20">
                    <div className="m-form-group m-error">
                        <input className="m-input_field" type="text" name="name" id="name" placeholder=" " />
                        <label className="m-input_label" for="name">Title*</label>
                    </div>
                    <div className="m-form-group">
                        <textarea type="text" className="input_field" name="review" id="review" placeholder=" " />
                        <label className="m-input_label" for="review">Review*</label>
                    </div>
                    <div className="m-form-group">
                        <button className="btn-blue">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default ReviewModal;