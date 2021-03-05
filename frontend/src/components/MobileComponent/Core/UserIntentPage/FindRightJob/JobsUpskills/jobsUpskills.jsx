import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
// import 'slick-carousel/slick/slick.css';
import '../../../SkillPage/CoursesTray/courses.scss';
import './jobsUpskills.scss';
import { useSelector } from 'react-redux';
import Loader from '../../../../Common/Loader/loader';
import { fetchFindRightJobsData, fetchUpskillYourselfData, upskillAndJobsCleanup } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import { startJobsUpskillsLoader, stopJobsUpskillsLoader } from 'store/Loader/actions';
import JobListing from './JobListing/jobListing';
import CourseLisiting from '../../IntentUtil/courseListing';
import Feedback from '../../IntentUtil/feedback';
import { showSwal } from 'utils/swal';

const JobsUpskills = (props) => {
    const dispatch = useDispatch();
    const { history } = props;
    const { jobsUpskillsLoader } = useSelector(store => store.loader);
    const { jobsList : { results, next } } = useSelector(store => store.findRightJob);
    const { course_data, page, recommended_course_ids }  = useSelector(store => store.upskillYourself);
    const params = new URLSearchParams(props.location.search);
    const [currentJobPage, setJobPage] = useState(1);
    const [selectTab, tabSelected] = useState('tab1');
    const openSelectedTab = (id) => { tabSelected(id); setFeedback(false) };
    const feedD = {'recommended_course_ids': recommended_course_ids, 'intent': 2, 'context': 'Find the right job'};
    const [feedback, setFeedback] = useState(false);

    useEffect(() => {
        resultApiFunc(history.location.search + `&page=1`);
        
        // Cleaning Store Bucket
        return function cleanup () {
			dispatch(upskillAndJobsCleanup())
		}
    }, []);

    const resultApiFunc = async (jobParams) => {
        // api hit for jobs for you
        try {
            dispatch(startJobsUpskillsLoader());
            await new Promise((resolve, reject) => dispatch(fetchFindRightJobsData({ jobParams, resolve, reject })));
        }
        catch (e) {
            history.push({
                search: ``
            });
            showSwal('error', 'Something went wrong! Try Again')
        }
        dispatch(stopJobsUpskillsLoader());
    }

    const handleUpskillData = async (tabType) => {
        setFeedback(false);
        if (tabType === "tab2" && (!course_data || (Array.isArray(course_data) && course_data.length === 0))) {
            const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage}&intent=2`;
            courseDispatchHit(dataUpskill);
        }
        openSelectedTab(tabType);
    }

    const courseDispatchHit = async (dataUpskill) => {
        dispatch(startJobsUpskillsLoader());

        // api hit for upskill yourself
        try {
            await new Promise((resolve, reject) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve, reject })));
            openSelectedTab('tab2');
        }
        catch(e) {
            showSwal('error', 'Something went wrong! Try Again');
            openSelectedTab('tab1');
        }
        dispatch(stopJobsUpskillsLoader());
    }

    const loadMoreJobs = (url_next) => {
        let next_data = url_next.split('json&');
        history.push({
            search: `?${next_data[1]}`
        });

        resultApiFunc(`?${next_data[1]}`);
    }

    const loadMoreCourses = (ev) => {
        ev.preventDefault();
        setJobPage(state => state+1);
        const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage + 1}&intent=2`;
        courseDispatchHit(dataUpskill);
    }

    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            { jobsUpskillsLoader ? <Loader /> : ''}
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-completed" to={"#"}>2</Link>
                        <Link className="m-current" to={"#"}>3</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <div className="m-jobs-upskills mt-20">
                    <div className="m-tabset-intent">
                        <input checked={selectTab === 'tab1'} onClick={() => openSelectedTab('tab1')} type="radio" name="tabset" id="tab1" aria-controls="Jobs for you" />
                        <label htmlFor="tab1">Jobs for you</label>

                        <input checked={selectTab === 'tab2'} onClick={() => handleUpskillData('tab2')} type="radio" name="tabset" id="tab2" aria-controls="Upskill yourself" />
                        <label htmlFor="tab2">Upskill yourself</label>

                        <div className="tab-panels">
                            <div id="tab1" className="tab-panel">
                                <JobListing jobList={results}/>
                                {next && <span className="m-load-more btn-col" onClick={() => loadMoreJobs(next)}>View More Jobs</span>}
                            </div>
                            <div id="tab2" className="tab-panel">
                                <div className="m-courses mt-20">
                                    <CourseLisiting courseList={course_data} />
                                </div>
                                {page?.has_next && <span className="m-load-more btn-col" onClick={loadMoreCourses}>View More Courses</span>}
                            </div>
                        </div>
                    </div>
                </div>
                { (results && results.length > 0) && <Feedback feed={feedback} setFeedback={setFeedback} feedbackData={feedD} heading={selectTab === 'tab1' ? 'jobs' : 'courses'}/> }
            </div>
        </section>
    )
}

export default JobsUpskills;