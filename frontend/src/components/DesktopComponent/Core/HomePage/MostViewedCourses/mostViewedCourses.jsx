import React, { useState } from 'react';
import './mostViewedCourses.scss';
import { Tabs, Tab } from 'react-bootstrap';
import PopularCourse from './popularCourse/popularCourse';
import { categoryTabs } from 'utils/constants';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMostViewedCourses } from 'store/HomePage/actions';
import useLearningTracking from 'services/learningTracking';

function MostViewedCourses() {
    
    const [key, setKey] = useState('-1');
    const dispatch = useDispatch()
    const { mostViewedCourses } = useSelector(store => store.mostViewed)
    const sendLearningTracking = useLearningTracking();

    const handleTabChange = async (tabType, key) => {
        
        if (!mostViewedCourses[tabType] || mostViewedCourses[tabType].length === 0)  {
            dispatch(startHomePageLoader())
            await new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ payload:{categoryId: tabType}, resolve, reject })));
            dispatch(stopHomePageLoader())
        }
        setKey(tabType);

        sendLearningTracking({
            productId: '',
            event: `homepage_most_viewed_course_${tabType}_${key}_tab_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'most_viewed_courses',
            eventCategory: tabType,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: key,
        })
    }



    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="recent-courses mt-20 mb-30">
                        <h2 className="heading2 text-center mb-25">Most viewed courses</h2>
                        <Tabs
                            id="controlled-tab-example"
                            activeKey={key}
                            onSelect={(tabType) => handleTabChange(tabType, key)}
                            className="category"
                        >

                            {
                                categoryTabs?.map((category) => {
                                    return (
                                        <Tab eventKey={category.id} title={<span>{category.name}</span>} key={category.id}>
                                            <ul className="recent-courses__list">
                                                {
                                                    mostViewedCourses[key]?.map((course, idx) => <PopularCourse course={course} indx={idx} key={idx} category={category?.name.replace(/ /gi, '_')}/>)
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