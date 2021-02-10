import React, { useState } from 'react';
import './mostViewedCourses.scss';
import { Tabs, Tab } from 'react-bootstrap';
import PopularCourse from './popularCourse/popularCourse';
import { categoryTabs } from 'utils/constants';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMostViewedCourses } from 'store/HomePage/actions';

function MostViewedCourses() {
    const [key, setKey] = useState('categories1');
    const dispatch = useDispatch()

    const handleTabChange = async (tabType) => {
        dispatch(startHomePageLoader())
        await new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ categoryId: tabType, resolve, reject})));
        dispatch(stopHomePageLoader())
        setKey(tabType)
    }

    const { mostViewedCourses } = useSelector( store => store.mostViewed )

    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="recent-courses mt-10 mb-10">
                        <h2 className="heading2 text-center">Most viewed courses</h2>
                        <Tabs
                            id="controlled-tab-example"
                            activeKey={key}
                            onSelect={(tabType) => handleTabChange(tabType)}
                            className="category"
                        >

                            {
                                categoryTabs?.map((category, index) => {
                                    return (
                                        <Tab eventKey={category.id} title={<span>{category.name}</span>} key={category.id}>
                                            <ul className="recent-courses__list">
                                                {
                                                    mostViewedCourses?.map((course, idx) =>  <PopularCourse course={course} /> )
                                                } 
                                            </ul>
                                        </Tab>
                                    )
                                })
                            }
                        </Tabs>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default MostViewedCourses;