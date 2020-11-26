import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import '../CoursesTray/courses.scss';
import { fetchPopulerCourses } from 'store/SkillPage/PopularCourses/actions'

const PopularCourses = (props) => {
    const dispatch = useDispatch()
    useEffect(() => {
        dispatch(fetchPopulerCourses({'medium' : 1}))
    }, [])
    const { pCourseList } = useSelector(store => store.popularCourses)

    const starRatings = (star) => {
        return (star === '*' ? <em className="icon-fullstar"></em> : star === '+' 
            ? <em className="icon-halfstar"></em> : <em className="icon-blankstar"></em>
        )
    }

    return (
    <section className="m-container m-courses mt-0 mb-0 pb-0">
        <div className="d-flex">
            <h2 className="m-heading2 mb-10">Popular Courses</h2>
            <Link className="ml-auto m-view-course" to={"#"}>View all courses</Link>
        </div>
        <div className="d-flex m-popular-courses">
        {
            pCourseList?.map((course) => {
                return (
                    <div className="m-col" id={course.id}>
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src={course.img} alt={course.img_alt} />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={course.url}>{course.name}</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="mr-10">By Simplilearn</span>
                                <span className="m-rating">
                                    { course.stars?.map((star) => starRatings(star)) }
                                    <span>{course.rating}/5</span>
                                </span>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })
        }
        </div>
    </section>
    );
  }

export default PopularCourses; 