import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './jobsUpskills.scss';
import JobListing from './JobListing/jobListing';
import CourseListing from '../../IntentUtil/courseListing';
import Feedback from '../../IntentUtil/feedback';
import { fetchFindRightJobsData, fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import { useDispatch, useSelector } from 'react-redux';
import { startJobsUpskillsLoader, stopJobsUpskillsLoader } from 'store/Loader/actions/index';
import Loader from 'components/DesktopComponent/Common/Loader/loader';


const JobsUpskills = (props) => {
	const [key, setKey] = useState('Jobs');
	const { location } = props
	const dispatch = useDispatch();
	const params = new URLSearchParams(props.location?.search);
	const [currentJobPage, setJobPage] = useState(1);
	const { jobsUpskillsLoader } = useSelector(store => store.loader);
	const { jobsList: { results, num_pages } } = useSelector(store => store.findRightJob)
	const { course_data, page } = useSelector(store => store.upskillYourself);

	const handleSelect = async (tabType) => {
		if (key !== tabType) {
			if (tabType === "Courses" && (!course_data || (Array.isArray(course_data) && course_data.length === 0))) {
				const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage}`;
				dispatch(startJobsUpskillsLoader())
				await new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
				dispatch(stopJobsUpskillsLoader())
			}
			setKey(tabType)
		}
	}

	const handleEffect = async () => {
		const jobParams = location?.search + `&page=1`;
		dispatch(startJobsUpskillsLoader())
		await new Promise((resolve, reject) => dispatch(fetchFindRightJobsData({ jobParams, resolve, reject })));
		dispatch(stopJobsUpskillsLoader())
	}

	useEffect(() => {

		handleEffect()
	}, [])

	

	const handleNextPage = async () => {
		//   const data = {
		//     'job': params.get('job'),
		//     'location': params.get('location'), //Is document work on SSR?
		//     'skills': params.get('skills'),
		//     'experience': params.get('experience'),
		//     'page': currentJobPage
		//   };
		//   dispatch(startJobsUpskillsLoader());
		//   await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
		//   dispatch(stopJobsUpskillsLoader());
		//   setJobPage(currentJobPage + 1);
		//   window.scrollTo({
		//     top: 0,
		//     left: 0,
		//     behavior: "smooth"
		//   });
	}

	const handleGotoFirstPage = async () => {
		//   const data = {
		//     'job': params.get('job'),
		//     'location': params.get('location'), //Is document work on SSR?
		//     'skills': params.get('skills'),
		//     'experience': params.get('experience'),
		//     'page': currentJobPage
		//   };
		//   dispatch(startJobsUpskillsLoader());
		//   await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
		//   dispatch(stopJobsUpskillsLoader());
		//   setJobPage(1);
		//   window.scrollTo({
		//     top: 0,
		//     left: 0,
		//     behavior: "smooth"
		//   });
	}

	const loadMoreCourses = async (eve) => {
		eve.preventDefault();
		const dataUpskill = `?preferred_role=${params.get('job_title')}&experience=${params.get('minexp')}&skills=${params.get('skill') || ''}&page=${currentJobPage + 1}`;
		dispatch(startJobsUpskillsLoader())
		await new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
		dispatch(stopJobsUpskillsLoader())
		setJobPage(state => state + 1)
	}

	return (
		<section className="container-fluid mt-30n mb-0">
			{ jobsUpskillsLoader ? <Loader /> : ''}
			<div className="row">
				<div className="container">
					<div className="ui-main col">
						<div className="ui-steps">
							<Link className="completed" to={"#"}>1</Link>
							<Link className="completed" to={"#"}>2</Link>
							<Link className="current" to={"#"}>3</Link>
						</div>
						<div className="jobs-upskills courses-tray mt-20 mr-15p">
							<Tabs
								id="controlled-tab-example"
								activeKey={key}
								onSelect={handleSelect}
								className="jobs-upskills"
							>

								<Tab eventKey="Jobs" title={<h2>Jobs for you</h2>}>
									<JobListing jobList={results} />
									{num_pages === currentJobPage ? <a onClick={handleGotoFirstPage} className="load-more" style={{ cursor: 'pointer' }}>View first Page</a> : <a onClick={handleNextPage} className="load-more" style={{ cursor: 'pointer' }}>View More Jobs</a>}
								</Tab>
								<Tab eventKey="Courses" title={<h2>Upskill yourself</h2>}>
									<CourseListing courseList={course_data} />
									{page && page.has_next ? <Link onClick={loadMoreCourses} className="load-more">View More Courses</Link> : ''}
								</Tab>
							</Tabs>
						</div>
						<Feedback/>
					</div>
				</div>
			</div>
		</section >
	)
}

export default JobsUpskills;