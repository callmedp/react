import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import '../../../SkillPage/CoursesTray/courses.scss'
import '../../FindRightJob/JobsUpskills/jobsUpskills.scss';
import CourseLisiting from '../../IntentUtil/courseListing';
import Feedback from '../../IntentUtil/feedback';
import { useDispatch, useSelector } from 'react-redux';
import { startCareerChangeLoader, stopCareerChangeLoader } from 'store/Loader/actions/index';
import { fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import Loader from '../../../../Common/Loader/loader';
import { showSwal } from 'utils/swal';

const ViewCourses = (props) => {
    const dispatch = useDispatch();
    const { history, match } = props;
    console.log(props);
    const params = new URLSearchParams(props.location?.search);
    const { course_data, page,recommended_course_ids } = useSelector(store => store.upskillYourself);
    const { careerChangeLoader } = useSelector(store => store.loader);
    let currentPage = 1;
    let intentValue = match?.params?.name === 'make-career-change' ? 0 : 1;
    const feedD = {'recommended_course_ids': recommended_course_ids, 'intent': intentValue, 'context': 'Make a career change'};

    useEffect(() => {
        handleUpskillData();
    }, []);

    const handleUpskillData = async() => {
        const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentPage}&intent=${intentValue}&department=${params.get('department')}`;
        dispatch(startCareerChangeLoader());
        
        // api hit for upskill yourself
        try {
            await new Promise((resolve, reject) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve, reject })));
        }
        catch(e) {
            showSwal('error', 'Something went wrong! Try Again');
            history.push({
				search: ``
			});
        }
        dispatch(stopCareerChangeLoader());
    }

    const loadMoreCourses = (curr_page) => {
        currentPage = curr_page+1;
        handleUpskillData();
    }

    return (
        <>
        { careerChangeLoader ? <Loader /> : '' }
            <section className="m-container mt-0 mb-0 pl-0 pr-0">
                <div className="m-ui-main col">
                    <div className="d-flex align-items-center">
                        <div className="m-ui-steps">
                            <Link className="m-completed" to={"#"}>1</Link>
                            <Link className="m-completed" to={"#"}>2</Link>
                            <Link className="m-current" to={"#"}>3</Link>
                        </div>
                        <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                    </div>
                    <h2 className="m-heading3 mt-20">Here’s how you can make a new career</h2>
                    <div className="m-jobs-upskills mt-20">
                        <div className="m-courses mt-20">
                            <CourseLisiting courseList={course_data} />
                        </div>
                        {page?.has_next && <span className="load-more btn-col" onClick={() => loadMoreCourses(page?.current_page)}>View More Courses</span>}
                        <br/>
                    </div>
                    <Feedback feedbackData={feedD}/>
                </div>
            </section>
        </>
    )
}

export default ViewCourses;