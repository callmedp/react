import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './viewCourses.scss';
import CourseLisiting from '../../CourseListing/courseListing';


const ViewCourses = (props) => {
    const [key, setKey] = useState('categories1');

    const { userIntent } = useSelector(store => store.userIntent)

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
                            <h2 className="heading3">Here’s how you can make a new career</h2>
                            <CourseLisiting courseList={userIntent} />
                            <Link to={"#"} className="load-more">View More Courses</Link>
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

export default ViewCourses;