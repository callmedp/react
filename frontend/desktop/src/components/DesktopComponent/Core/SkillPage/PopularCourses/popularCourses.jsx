import React from 'react';
import { useSelector } from 'react-redux';
import { Link as LinkScroll } from 'react-scroll';
import './popularCourses.scss'
import { siteDomain } from 'utils/domains';

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
                                <a href={`${siteDomain}${course.url}`}>{course.name}</a>
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
            <LinkScroll to="courses" className="view-all" isDynamic={true} spy={true}  offset={-120}>View all courses</LinkScroll>
        </div>
    )
}

export default PopularCourses;