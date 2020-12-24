import React from 'react';
import { useDispatch, useSelector, connect } from 'react-redux';
import { Link as LinkScroll } from 'react-scroll';
import './popularCourses.scss'
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo, getTrackingParameters } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const PopularCourses = (props) => {

    const { trendingCourses } = useSelector( store => store.footer )
    const { userTrack, gaTrack } = props;
    const { heading } = useSelector( store => store.skillBanner )
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();

    const starRatings = (star) => {
        return (star === '*' ? <em className="icon-fullstar" key={Math.random()}></em> : star === '+' 
            ? <em className="icon-halfstar" key={Math.random()}></em> : <em className="icon-blankstar" key={Math.random()}></em>
        )
    }


    const trackingParameters = getTrackingParameters(tracking_data);

    const handleTracking = (course) => {
        gaTrack('SkillPopularCourses','ln_popular_course_select', 'ln_'+ course.name, heading,'', false, true);
        userTrack({"query" : tracking_data, "action" :'exit_skill_page' });
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
                                <a href={`${siteDomain}${course.url}${trackingParameters}`} onClick={() => handleTracking(course)}>{course.name}</a>
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
            <LinkScroll to="courses" className="view-all" isDynamic={true} spy={true}  offset={-120} onClick={()=> gaTrack('SkillPopularCourses','ln_popular_course_select', 'ln_view_courses', heading,'', false, true), () => userTrack({"query" : tracking_data, "action" :'exit_skill_page' }) }>View all courses</LinkScroll>
        </div>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "userTrack": (data) => {
            return dispatch(trackUser(data))
        },
        "gaTrack": (data) => { MyGA.SendEvent(data)
        }
    }
}

export default connect(null, mapDispatchToProps)(PopularCourses);
