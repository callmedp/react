import React from 'react';
import { Link } from 'react-router-dom';
import ReviewModal from '../Inbox/reviewModal';

const ReviewRating = (props) => {

    const { item, handleShow, 
        toggleReviews, setOpenReview,
        openReview, name } = props;

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
        { item.rating === null ?
            <span
                className="cursor-pointer mr-2 font-weight-bold"
                onClick={handleShow}
            >
                Rate {name}
            </span>
            : null
        }

        <span className="rating">
            { item.rating.map((val, ind) => <i key={ind} value={val} className={fillStarForCourse(val)}></i>)}
        </span>

        { item.rating?.length  ?
            <React.Fragment>
                <span>{item.avg_rating}/5</span>
                <Link
                    className="ml-15"
                    onClick={() => toggleReviews(item.id)}
                    aria-controls="threeComments"
                    aria-expanded={`openReview` + item.id}
                    to={'#'}
                >
                    <strong>{item.review}</strong> {item.review > 1 ? 'Reviews' : 'Review'}
                </Link>

                {/* modal for filled in reviews */}
                <ReviewModal  
                    handleShow={handleShow}
                    setOpenReview={setOpenReview} 
                    setOpenReview={openReview}
                    id={item.id}/>

            </React.Fragment>
            : null
        }
    </div>
    )
}

export default ReviewRating;
