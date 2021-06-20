import React from 'react'
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';
import { Link } from 'react-router-dom';

const PopularCourse = (props) => {
    const {course,category, indx} = props;
    const sendLearningTracking = useLearningTracking();

    const starRatings = (star) => {
        return (star === '*' ? <em className="icon-fullstar" key={Math.random()}></em> : star === '+' 
            ? <em className="icon-halfstar" key={Math.random()}></em> : <em className="icon-blankstar" key={Math.random()}></em>
        )
    }

    const mostViewedTracking = (name) => {
        let name_joined = name.replace(/ /g, '_');

        MyGA.SendEvent('ln_new_homepage','ln_most_viewed_course', 'ln_'+category, name_joined,'', false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_most_viewed_course_${category}_${name_joined}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'most_viewed_courses',
            eventCategory: `${name_joined}`,
            eventLabel: `${category}_${name_joined}`,
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <li className="col-sm-3">
        <div className="card">
            <div className="card__heading">
                <figure>
                    <img src={course.imgUrl} alt={course.imgAlt} />
                </figure>
                <h3 className="heading3">
                    <Link className="cursorLink" to={course.url} onClick={() => mostViewedTracking(course.name)}>{course.name}</Link>
                </h3>
            </div>
            <div className="card__box">
                <div className="card__rating">
                <span className="rating">
                    { course.stars?.map((star) => starRatings(star)) }
                    <span>{course.rating}/5</span>
                </span>
                {
                    course?.mode && <span className="mode">{course?.mode}</span>
                }
                </div>
                <div className="card__price mt-10">
                    <strong>{course.price}/-</strong> 
                </div>
            </div>
        </div>
    </li>
    )
}

export default PopularCourse;
