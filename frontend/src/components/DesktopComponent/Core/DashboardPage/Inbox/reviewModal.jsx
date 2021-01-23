import React from 'react';
import { Collapse } from 'react-bootstrap';

const ReviewModal = (props) => {
    const { handleShow, setOpenReview, openReview, item, setProductReview } = props;
    // console.log(setProductReview)

    return (
        <Collapse in={openReview == item.id}>
        <div className="db-reviews-list-wrap arrow-box top-big">
            <span className="btn-close"  onClick={() => setOpenReview(state => !state)}>&#x2715;</span>
            <div className="reviews-list">
                <ul>
                    {setProductReview && setProductReview[0]?.data?.data?.map((rev, idx) => {
                        return (
                            <li key={idx}>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>{rev.average_rating}</strong> /5</span>
                                    </span>
                                </div>

                                <span className="reviews-list--date">{rev.title ? rev.title : ""} {rev.created}</span>
                                <p className="reviews-list--text">{rev.content ? rev.content : ""}</p>
                            </li>
                        )
                    })}
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