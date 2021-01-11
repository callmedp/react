import React, { useState } from 'react';
import '../../SkillPage/CoursesTray/coursesTray.scss';
import { Tabs, Tab } from 'react-bootstrap';
import SnMCourses from 'components/DesktopComponent/Common/Product/product';
import ITCourses from 'components/DesktopComponent/Common/Product/product';
import BnFCourses from 'components/DesktopComponent/Common/Product/product';
import { useSelector } from 'react-redux';

function CoursesTray() {

    const [key, setKey] = useState('categories1');
    const [categoryKey1, setCategoryKey1] = useState(1);
    const [categoryKey2, setCategoryKey2] = useState(1);
    const [categoryKey3, setCategoryKey3] = useState(1);

    const { SnMCourseList, ITCourseList, BnFCourseList } = useSelector( store => store.popularCategories ) 
    

    const loadMoreCourses = (setCategoryKey) => {
        setCategoryKey( state => state+1);
    }

    return (
        <section className="container mt-30">
            <div className="row">
                <div className="col courses-tray" data-aos="fade-up">
                    <h2 className="heading2 text-center mb-20">Recommended Categories</h2>
                    <Tabs
                        id="controlled-tab-example"
                        activeKey={key}
                        onSelect={(k) => setKey(k)}
                        className="category"
                    >

                        <Tab eventKey="categories1" title={<h2>Sales and Marketing</h2>}>
                            {
                                SnMCourseList.slice(0, categoryKey1).map((courses, index) => {
                                    return (
                                        <ul className="courses-tray__list" key={index} >
                                            {
                                                courses.map((course, idx) => <SnMCourses listIdx={idx} index={index.toString() + idx.toString()} product={course} key={index.toString() + idx.toString()} />)
                                            }
                                        </ul>
                                    )
                                })
                            }
                            { categoryKey1 < SnMCourseList.length ? <a type="button" onClick={() => loadMoreCourses(setCategoryKey1)} className="load-more pt-30">Load More Courses</a> : ''}

                        </Tab>
                        <Tab eventKey="categories2" title={<h2>Information Technology</h2>}>
                            {
                                ITCourseList.slice(0, categoryKey2).map((courses, index) => {
                                    return (
                                        <ul className="courses-tray__list" key={index} >
                                            {
                                                courses.map((course, idx) => <ITCourses listIdx={idx} index={index.toString() + idx.toString()} product={course} key={index.toString() + idx.toString()} />)
                                            }
                                        </ul>
                                    )
                                })
                            }
                            { categoryKey2 < ITCourseList.length ? <a type="button" onClick={() => loadMoreCourses(setCategoryKey2)} className="load-more pt-30">Load More Courses</a> : ''}
                        </Tab>
                        <Tab eventKey="categories3" title={<h2>Banking & Finance</h2>}>
                            {
                                BnFCourseList.slice(0, categoryKey3).map((courses, index) => {
                                    return (
                                        <ul className="courses-tray__list" key={index} >
                                            {
                                                courses.map((course, idx) => <BnFCourses listIdx={idx} index={index.toString() + idx.toString()} product={course} key={index.toString() + idx.toString()} />)
                                            }
                                        </ul>
                                    )
                                })
                            }
                            { categoryKey3 < BnFCourseList.length ? <a type="button" onClick={() => loadMoreCourses(setCategoryKey3)} className="load-more pt-30">Load More Courses</a> : ''}
                        </Tab>

                    </Tabs>
                </div>
            </div>
        </section>
    );
}

export default CoursesTray;