import React from 'react';
import { Collapse } from 'react-bootstrap';

const ReviewModal = (props) => {
    const { handleShow, setOpenReview, openReview, item, setProductReview } = props;

    const fillStarForCourse = (star) => {
        return {
            '*': 'icon-fullstar',
            '+': 'icon-halfstar',
            '-': 'icon-blankstar'
        }[star];
    }
    console.log(setProductReview)

    return (
        <Collapse in={openReview == item.id}>
        <div className="db-reviews-list-wrap arrow-box top-big">
            <span className="btn-close"  onClick={() => setOpenReview(state => !state)}>&#x2715;</span>
            <div className="reviews-list">
                <ul>
                    {setProductReview?.length > 0 && setProductReview.map((rev, idx) => {
                        return (
                            <li key={idx}>
                                <div className="card__rating">
                                    { rev.rating.map((val, ind) => <i key={ind} value={val} className={fillStarForCourse(val)}></i>)}
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