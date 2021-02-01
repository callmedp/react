import React from 'react';
import { Collapse } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import Loader from '../../../Common/Loader/loader';

const ReviewModal = (props) => {
    const { handleShow, setOpenReview, openReview, item } = props;

    const fillStarForCourse = (star) => {
        return {
            '*': 'icon-fullstar',
            '+': 'icon-halfstar',
            '-': 'icon-blankstar'
        }[star];
    }

    const { reviewList } = useSelector(store => store.getReviews.reviewList);
    const { reviewLoader } = useSelector(store => store.loader);

    return (
        <>
            { reviewLoader && <Loader /> }
        <Collapse in={openReview == item.id}>
        <div className="db-reviews-list-wrap arrow-box top-big">
            <span className="btn-close"  onClick={() => setOpenReview(state => !state)}>&#x2715;</span>
            <div className="reviews-list">
                <ul>
                    { reviewList?.map((rev, idx) => {
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
    </>
    )
}

export default ReviewModal;