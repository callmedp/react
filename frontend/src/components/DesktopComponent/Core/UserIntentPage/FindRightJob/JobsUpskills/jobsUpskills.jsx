import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './jobsUpskills.scss';
import JobListing from './JobListing/jobListing';
import CourseListing from '../../CourseListing/courseListing';

import Loader from '../../../../Common/Loader/loader';
import { fetchFindRightJobsData, fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import { startJobsUpskillsLoader, stopJobsUpskillsLoader } from 'store/Loader/actions';
import { siteDomain } from 'utils/domains';
import { useDispatch, useSelector } from 'react-redux';


const JobsUpskills = (props) => {
    const params = new URLSearchParams(props.location.search);
    const [key, setKey] = useState('categories1');
    const dispatch = useDispatch();
    const [ currentJobPage, setJobPage ] = useState(!!params.get('page') ? parseInt(params.get('page')) + 1 : 1);
    const { jobsUpskillsLoader } = useSelector(store => store?.loader);
    const { jobsList, num_pages } = useSelector(store => store?.findRightJob);
    const { course_data, page, recommendate_ids} = useSelector(store => store?.upskillYourself.upskillList);

    

    useEffect( async () => {
        const data = {
            'job': params.get('job'),
            'location': params.get('location'), //Is document work on SSR?
            'skills': params.get('skills'),
            'experience': params.get('experience'),
            'page': currentJobPage
        };

        if(!jobsList?.results) {
            dispatch(startJobsUpskillsLoader());
            await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
            dispatch(stopJobsUpskillsLoader());
        }
    }, []);

    function handleSkillData() {
        dispatch(startJobsUpskillsLoader());
        const dataUpskill = {
            'preferred_role': params.get('job_title'),
            'skills': params.get('skills'),
            'experience': params.get('experience')
        };
        // api hit for upskill yourself
        if(!course_data) {
            new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
            dispatch(stopJobsUpskillsLoader());
        }
    }

    const handleNextPage = async () => {
        const data = {
            'job': params.get('job'),
            'location': params.get('location'), //Is document work on SSR?
            'skills': params.get('skills'),
            'experience': params.get('experience'),
            'page': currentJobPage
        };
        dispatch(startJobsUpskillsLoader());
        await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
        dispatch(stopJobsUpskillsLoader());
        setJobPage(currentJobPage + 1);
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
    }

    const handleGotoFirstPage = async () => {
        const data = {
            'job': params.get('job'),
            'location': params.get('location'), //Is document work on SSR?
            'skills': params.get('skills'),
            'experience': params.get('experience'),
            'page': currentJobPage
        };
        dispatch(startJobsUpskillsLoader());
        await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
        dispatch(stopJobsUpskillsLoader());
        setJobPage(1);
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
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
                            onSelect={(k) => setKey(k)}
                            className="jobs-upskills"
                            >
                    
                                <Tab eventKey="categories1" title={<h2>Jobs for you</h2>}>
                                    <JobListing jobList={jobsList?.results}/>
                                    { jobsList?.num_pages === currentJobPage ?  <a onClick={handleGotoFirstPage} className="load-more" style={{cursor: 'pointer'}}>View first Page</a> : <a onClick={handleNextPage} className="load-more" style={{cursor: 'pointer'}}>View More Jobs</a> }
                                </Tab>
                                <Tab eventKey="categories2" onClick={handleSkillData} title={<h2>Upskill yourself</h2>}>
                                    <CourseListing courseList={[]} />
                                    <Link to={"#"} className="load-more">View More Courses</Link>
                                </Tab>
                            </Tabs>
                        </div>
                        <div className="courses-feedback mt-50 mr-15p">
                            <strong>Are these courses recommendation relevant to your profile?</strong>
                            <span className="ml-auto">
                                <Button variant="outline-primary">Yes</Button>{' '}
                                <Button variant="outline-primary">No</Button>{' '}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default JobsUpskills;