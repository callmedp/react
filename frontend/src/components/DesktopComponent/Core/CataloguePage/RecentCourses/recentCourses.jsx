import React from 'react';
import './recentCourses.scss';
import { siteDomain } from 'utils/domains';
import { useSelector } from 'react-redux';

const RecentCourses = (props) => {

    const { recentCoursesList } = useSelector(store => store.recentCourses);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    return (
        <section className="container-fluid lightblue-bg mt-30" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="recent-courses mt-40 mb-50">
                        <h2 className="heading2 text-center">Recently added courses</h2>
                        <ul className="recent-courses__list">
                            {
                                recentCoursesList?.slice(0,4).map((course, index) => {
                                    return (
                                        <li className="col" key={index}>
                                            <div className="card">
                                                <div className="card__heading">
                                                    <figure>
                                                        <img src={course.imgUrl} alt={course.imgAlt} />
                                                    </figure>
                                                    <h3 className="heading3">
                                                        <a to={`${siteDomain}${course.url}`}>{course.name}</a>
                                                    </h3>
                                                </div>
                                                <div className="card__box">
                                                    <div className="card__rating">
                                                        <span className="mr-10">By {course.provider}</span>

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
                                })
                            }

                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default RecentCourses;