import React from 'react'
import { siteDomain } from 'utils/domains';

const popularCourse = (props) => {
    const {course} = props

    const starRatings = (star) => {
        return (star === '*' ? <em className="icon-fullstar" key={Math.random()}></em> : star === '+' 
            ? <em className="icon-halfstar" key={Math.random()}></em> : <em className="icon-blankstar" key={Math.random()}></em>
        )
    }
    return (
        <li className="col">
        <div className="card">
            <div className="card__heading">
                <figure>
                    <img src={course.img} alt={course.img_alt} />
                </figure>
                <h3 className="heading3">
                    <a to={`${siteDomain}${course.url}`}>{course.name}</a>
                </h3>
            </div>
            <div className="card__box">
                <div className="card__rating">
                <span className="rating">
                    { course.stars?.map((star) => starRatings(star)) }
                    <span>{course.rating}/5</span>
                </span>
                <span className={course.mode}>Online</span>
                </div>
                <div className="card__price mt-10">
                    <strong>{course.price}/-</strong> 
                </div>
            </div>
        </div>
    </li>
    )
}

export default popularCourse;
