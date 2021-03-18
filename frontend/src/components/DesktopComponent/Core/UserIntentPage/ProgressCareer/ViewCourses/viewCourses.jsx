import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './viewCourses.scss';
import CourseLisiting from '../../IntentUtil/courseListing';
import Feedback from '../../IntentUtil/feedback';
import { fetchUpskillYourselfData, upskillAndJobsCleanup } from 'store/UserIntentPage/actions';
import { startCareerChangeLoader, stopCareerChangeLoader } from 'store/Loader/actions/index';
import Loader from 'components/DesktopComponent/Common/Loader/loader';

const ViewCourses = (props) => {
    const { course_data, page, recommended_course_ids } = useSelector(store => store.upskillYourself);
    const dispatch = useDispatch()
    const { careerChangeLoader } = useSelector(store => store.loader);
    const [currentJobPage, setJobPage] = useState(1);
    const params = new URLSearchParams(props.location?.search);
    const feedD = {'recommended_course_ids': recommended_course_ids, 'intent': 1, 'context': 'Progress your career'};
    const [feedback, setFeedback] = useState(false);

    const handleEffect = async () => {
		const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage}&intent=1&department=${params.get('department')}`; //need to revied
		dispatch(startCareerChangeLoader())
        await new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
		dispatch(stopCareerChangeLoader())
	}
    
    useEffect(() => {
        handleEffect()

        // Cleaning Store Bucket
        return function cleanup () {
        dispatch(upskillAndJobsCleanup())
        }
    },[])

    const loadMoreCourses = async (eve) => {
        eve.preventDefault();
		const dataUpskill =  `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage + 1}&intent=1&department=${params.get('department')}`;
        
        dispatch(startCareerChangeLoader())
            await new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
		dispatch(stopCareerChangeLoader())
		setJobPage(state => state + 1)
	}

    return (
        <section className="container-fluid mt-30n mb-0">
            { careerChangeLoader ? <Loader /> : ''}
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="completed" to={"#"}>2</Link>
                            <Link className="current" to={"#"}>3</Link>
                        </div>

                        <div className="jobs-upskills courses-tray mt-20 mr-15p">
                            <h2 className="heading3">Here’s how you can make a new career</h2>
                            <CourseLisiting courseList={course_data} />
                            {page && page.has_next ? <Link onClick={loadMoreCourses} className="load-more">View More Courses</Link> : ''}
                        </div>
                        <Feedback feed={feedback} setFeedback={setFeedback} feedbackData={feedD} heading={'courses'} />
                    </div>
                </div>
            </div>
        </section>
    )
}

export default ViewCourses;