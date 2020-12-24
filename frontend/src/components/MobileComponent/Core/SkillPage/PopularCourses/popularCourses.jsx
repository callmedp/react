import React, { useEffect } from 'react';
import { useDispatch, useSelector, connect } from 'react-redux';
import { Link } from 'react-router-dom';
import '../CoursesTray/courses.scss';
import './popularCourses.scss';
import { fetchTrendingCnA } from 'store/Footer/actions/index';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo, getTrackingParameters } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const PopularCourses = (props) => {
    const { setTabType } = props
    const dispatch = useDispatch()
    const tracking_data = getTrackingInfo();
    useEffect(() => {
        dispatch(fetchTrendingCnA())
    }, [])

    const { trendingCourses } = useSelector( store => store.footer )
    const { heading } = useSelector( store => store.skillBanner )

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const trackingParameters = getTrackingParameters(tracking_data);
    const { trackUser } = props;

    const handleTracking = () => {
        e.preventDefault();
        setTabType('courses');
        MyGA.SendEvent('SkillPopularCourses','ln_popular_course_select', 'ln_view_courses', heading,'', false, true);
        trackUser({"query" : tracking_data, "action" :'exit_skill_page'});
    }

    return (
        <>
        {
            trendingCourses.length ? 
            (
                <section className="m-container m-courses mt-0 mb-0 pt-10 pb-0">
                    <div className="d-flex">
                        <h2 className="m-heading2 mb-10">Popular Courses</h2>
                        <a href="#" className="ml-auto m-view-course" onClick={handleTracking}>View all courses</a>
                    </div>
                    <div className="d-flex m-popular-courses">
                    {
                        trendingCourses?.slice(0,2).map((course) => {
                            return (
                                <div className="m-col" key={course.id}>
                                    <div className="m-card">
                                        <div className="m-card__heading">
                                            <figure>
                                                <img src={course.img} alt={course.img_alt} />
                                            </figure>
                                            <h3 className="m-heading3 m-pop">
                                                <a href={`${course.url}${trackingParameters}`} onClick={ () => MyGA.SendEvent('SkillPopularCourses','ln_popular_course_select', 'ln_'+ course.name, heading,'', false, true)}>{course.name}</a>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating">
                                            <span className="mr-10">By {course.provider}</span>
                                            <span className="m-rating">
                                                { course.stars?.map((star, index) => starRatings(star, index)) }
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
            ): null
        }
        </>
    );
  }

const mapDispatchToProps = (dispatch) => {
    return {
        "trackUser": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(PopularCourses);