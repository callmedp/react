import React from 'react';
import { siteDomain } from 'utils/domains';

const CourseCard = (props) => {

    const { course } = props;
    
    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    return (
        <li className="col">
        <div className="card">
            <div className="card__heading">
                <figure>
                    <img src={course.imgUrl} alt={course.imgAlt} />
                </figure>
                <h3 className="heading3">
                    <a href={`${siteDomain}${course.url}`}>{course.name}</a>
                </h3>
            </div>
            <div className="card__box">
                <div className="card__rating">
                    <span className="mr-10">By {course.providerName}</span>

                    <span className="rating">
                        {course.stars?.map((star, index) => starRatings(star, index))}
                        <span>{course.rating?.toFixed(1)}/5</span>
                    </span>
                </div>
                <div className="card__price mt-10">
                    <strong>{course.price}/-</strong>
                </div>
            </div>
        </div>
    </li>
    )
}

export default CourseCard;
