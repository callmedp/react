import React, {useState} from 'react';
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
import { useDispatch } from 'react-redux';


const JobsUpskills = (props) => {
    const [key, setKey] = useState('categories1');
    const dispatch = useDispatch();

    return (
        <section className="container-fluid mt-30n mb-0">
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
                                    <JobListing/>
                                    <Link to={"#"} className="load-more">View More Jobs</Link>
                                </Tab>
                                <Tab eventKey="categories2" title={<h2>Upskill yourself</h2>}>
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