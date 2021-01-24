import React from 'react';
import { Link } from 'react-router-dom';
import ReviewModal from '../Inbox/reviewModal';

const ReviewRating = (props) => {
    const { item, handleShow, toggleReviews, setOpenReview, openReview, name, setProductReview } = props;

      // fill starts of already rated courses
      const fillStarForCourse = (star) => {
        return {
            '*': 'icon-fullstar',
            '+': 'icon-halfstar',
            '-': 'icon-blankstar'
        }[star];
    }

    return (
        <div className="card__rating">
        { item.no_review != 0 ?
            <React.Fragment>
                <span className="rating">
                    { item.rating.map((val, ind) => <i key={ind} value={val} className={fillStarForCourse(val)}></i>)}
                </span>

                <span>{item.avg_rating}/5</span>
                
                <Link
                    className="ml-15"
                    onClick={() => toggleReviews(item.id, item.product)}
                    aria-controls="threeComments"
                    aria-expanded={`openReview` + item.id}
                    to={'#'}
                >
                    <strong>{item.no_review}</strong> {item.no_review > 1 ? 'Reviews' : 'Review'}
                </Link>

                {/* modal for filled in reviews */}
                <ReviewModal  
                    handleShow={handleShow}
                    setOpenReview={setOpenReview} 
                    openReview={openReview}
                    item={item}
                    setProductReview={setProductReview}/>

            </React.Fragment>
            :
            // if no of review is zero
            <React.Fragment>
                <span
                    className="cursor-pointer mr-2 font-weight-bold"
                    onClick={handleShow}
                >
                    Rate {name}
                </span>

                <span className="rating">
                    { item.rating.map((val, ind) => <i key={ind} value={val} className="icon-blankstar"></i>)}
                </span>
            </React.Fragment>
        }
    </div>
    )
}

export default ReviewRating;
