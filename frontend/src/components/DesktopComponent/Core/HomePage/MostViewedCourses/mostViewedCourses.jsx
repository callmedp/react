import React, { useState } from 'react';
import './mostViewedCourses.scss';
import { Tabs, Tab } from 'react-bootstrap';
import PopularCourse from './popularCourse/popularCourse';
import { categoryTabs } from 'utils/constants';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMostViewedCourses } from 'store/HomePage/actions';

function MostViewedCourses() {
    
    const [key, setKey] = useState('-1');
    const dispatch = useDispatch()
    const { mostViewedCourses } = useSelector(store => store.mostViewed)

    const handleTabChange = async (tabType) => {
        
        if (!mostViewedCourses[tabType] || mostViewedCourses[tabType].length === 0)  {
            dispatch(startHomePageLoader())
            await new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ categoryId: tabType, resolve, reject })));
            dispatch(stopHomePageLoader())
        }
        setKey(tabType)
    }



    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="recent-courses mt-20 mb-30">
                        <h2 className="heading2 text-center mb-20">Most viewed courses</h2>
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
                                                    mostViewedCourses[key]?.map((course, idx) => <PopularCourse course={course} key={idx}/>)
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