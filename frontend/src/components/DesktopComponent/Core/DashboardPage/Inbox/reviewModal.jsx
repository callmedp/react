import React from 'react';
import { Collapse } from 'react-bootstrap';

const ReviewModal = (props) => {

    const { handleShow, setOpenReview, openReview, id } = props;

    return (
        <Collapse in={openReview == id}>
        <div className="db-reviews-list-wrap arrow-box top-big">
            <span className="btn-close"  onClick={() => setOpenReview(state => !state)}>&#x2715;</span>
            <div className="reviews-list">
                <ul>
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

                        <span className="reviews-list--date">Dec. 21, 2020</span>
                        <p className="reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                    </li>
                </ul>
            </div>
            
            <div className="db-reviews-list-wrap--bottom">
                <button className="btn btn-outline-primary" onClick={handleShow}>Add new</button>
            </div>
        </div>
    </Collapse>
    )
}

export default ReviewModal;