import React, { useEffect, useState } from 'react';
import './coursesTray.scss';
import { Tabs, Tab } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import Courses from './Product/product';
import Assessments from './Product/product';

const CoursesTray = (props) => {
    const [key, setKey] = useState('courses');
    const pageId = props.pageId
    const dispatch = useDispatch();
    const { courseList, assessmentList } = useSelector(store => store.coursesTray)
    const [ courseKey, setCourseKey ] = useState(2)
    const [ assessmentKey, setAssessmentKey ] = useState(2)

    const loadMoreCourses = () => {
        setCourseKey(state => state+1)
    }

    const loadMoreAssessments = () => {
        setAssessmentKey(state => state+1)
    }

    useEffect(() => {
        dispatch(fetchCoursesAndAssessments({ id: pageId }));
    }, [])


    return (
        <section className="container" id="courses">
            <div className="row">
                <div className="col courses-tray">
                    <Tabs
                        id="controlled-tab-example"
                        activeKey={key}
                        onSelect={(k) => setKey(k)} >

                        <Tab eventKey="courses" title="Courses">
                            {
                                courseList.slice(0, courseKey).map((courses, index) => {
                                    return (
                                        <ul className="courses-tray__list" key={index}>
                                            {
                                                courses.map((course, idx) => <Courses listIdx={idx+1} listSize={courses.length} index={index.toString() + idx.toString()} product={course} key={index.toString() + idx.toString()} />)
                                            }
                                        </ul>
                                    )
                                })
                            }
                            { courseKey < courseList.length ? <a type="button" onClick={loadMoreCourses} className="load-more pt-30">Load More Courses</a> : '' }
                        </Tab>

                        <Tab eventKey="assessments" title="Assessments">
                            {
                                assessmentList.slice(0,assessmentKey).map((assessments, index) => {
                                    return (
                                        <ul className="courses-tray__list" key={index}>
                                            {
                                                assessments.map((assessment, idx) =>  <Assessments listIdx={idx+1} listSize={assessments.length}  index={index.toString() + idx.toString()} product={assessment} key={index.toString() + idx.toString()} /> )
                                            }
                                    </ul>
                                    )
                                })
                            }
                            { assessmentKey < assessmentList.length ? <a type="button" onClick={loadMoreAssessments} className="load-more pt-30">Load More Assessments</a> : '' }
                        </Tab>
                    </Tabs>
                </div>
            </div>
        </section>
    );
}

export default CoursesTray;