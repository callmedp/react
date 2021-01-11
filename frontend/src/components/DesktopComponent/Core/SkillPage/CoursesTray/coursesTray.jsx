import React, { useEffect, useState } from 'react';
import './coursesTray.scss';
import { Tabs, Tab } from 'react-bootstrap';
import { useSelector, connect } from 'react-redux';

import Courses from './Product/product';
import Assessments from './Product/product';
import { MyGA } from 'utils/ga.tracking.js';

const CoursesTray = (props) => {

    const [key, setKey] = useState('courses');
    const { courseList, assessmentList } = useSelector(store => store.coursesTray)
    const [courseKey, setCourseKey] = useState(2)
    const [assessmentKey, setAssessmentKey] = useState(2)
    const { gaTrack, setHasCourses, pageId } = props;

    const loadMoreCourses = () => {
        gaTrack('SkillCourseLoadMore', 'ln_course_click', 'ln_know_more', 'ln_course', '', false, true)
        setCourseKey(state => state + 1)
    }

    const loadMoreAssessments = () => {
        gaTrack('SkillAssesmentLoadMore', 'ln_course_click', 'ln_know_more', 'ln_assessment', '', false, true)
        setAssessmentKey(state => state + 1)
    }

    useEffect(() => {
        setHasCourses( courseList.length > 0 )
    },[courseList])




    return (
        <section className="container" id="courses" data-aos="fade-up" data-aos-duration="1000">
            <div className="row">
                <div className="col courses-tray">
                    <Tabs
                        id="controlled-tab-example"
                        activeKey={key}
                        onSelect={(k) => setKey(k)} >
                        {
                            courseList.length ? <Tab eventKey="courses" title={<h2>{ pageId === '32' ? "All Digital Marketing " : ''}Courses</h2>}>
                                {
                                    courseList.slice(0, courseKey).map((courses, index) => {
                                        return (
                                            <ul className="courses-tray__list" key={index} >
                                                {
                                                    courses.map((course, idx) => <Courses listIdx={idx} index={index.toString() + idx.toString()} product={course} key={index.toString() + idx.toString()} productType='courses'/>)
                                                }
                                            </ul>
                                        )
                                    })
                                }
                                {courseKey < courseList.length ? <a type="button" onClick={loadMoreCourses} className="load-more pt-30">Load More Courses</a> : ''}
                            </Tab> : ''
                        }

                        {
                            assessmentList.length ? <Tab eventKey="assessments" title={<h2>Assessments</h2>}>
                                {
                                    assessmentList.slice(0, assessmentKey).map((assessments, index) => {
                                        return (
                                            <ul className="courses-tray__list" key={index}>
                                                {
                                                    assessments.map((assessment, idx) => <Assessments listIdx={idx} index={index.toString() + idx.toString()} product={assessment} key={index.toString() + idx.toString()} productType='assessments'/>)
                                                }
                                            </ul>
                                        )
                                    })
                                }
                                {assessmentKey < assessmentList.length ? <a type="button" onClick={loadMoreAssessments} className="load-more pt-30">Load More Assessments</a> : ''}
                            </Tab> : ''
                        }

                    </Tabs>
                </div>
            </div>
        </section>
    );
}

const mapDispatchToProps = (dispatch) => {
    return {
        "gaTrack": (data) => {
            MyGA.SendEvent(data)
        }
    }
}

export default connect(null, mapDispatchToProps)(CoursesTray);