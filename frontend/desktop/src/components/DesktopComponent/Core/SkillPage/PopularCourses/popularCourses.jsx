import React from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './popularCourses.scss'

const PopularCourses = (props) => {

    const { trendingCourses } = useSelector( store => store.footer )

    const starRatings = (star) => {
        return (star === '*' ? <em className="icon-fullstar" key={Math.random()}></em> : star === '+' 
            ? <em className="icon-halfstar" key={Math.random()}></em> : <em className="icon-blankstar" key={Math.random()}></em>
        )
    }

    return (
        <div className="popular-courses mt-40">
            <h2 className="heading2">Popular Courses</h2>
            <ul className="popular-courses__list">
            {
                trendingCourses?.slice(0,3).map((course) => {
                    return (
                        <li key={course.id}>
                            <figure>
                                <img src={course.img} alt={course.img_alt} />
                            </figure>
                            <div className="links">
                                <Link to={course.url}>{course.name}</Link>
                                <span className="mr-10">By {course.provider}</span>
                                    <span className="rating">
                                        { course.stars?.map((star) => starRatings(star)) }
                                        <span>{course.rating}/5</span>
                                    </span>
                            </div>
                        </li>
                    )
                })
            }
            </ul>
            <Link className="view-all" to={"#"}>View all courses</Link>
        </div>
    )
}

export default PopularCourses;