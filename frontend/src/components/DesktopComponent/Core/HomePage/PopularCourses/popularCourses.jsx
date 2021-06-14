import React, { useState } from 'react';
import '../../SkillPage/CoursesTray/coursesTray.scss';
import './popularCourses.scss'
import { Tabs, Tab } from 'react-bootstrap';
import MasterProduct from './HomeProduct/homeProduct';
import CertificationProduct from './HomeProduct/homeProduct';
import { useSelector, useDispatch } from 'react-redux';
import { fetchInDemandProducts } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import useLearningTracking from 'services/learningTracking';

function PopularCourses() {
    const [key, setKey] = useState('master');
    const { courses, certifications } = useSelector( store => store.inDemand )
    const dispatch = useDispatch();
    const sendLearningTracking = useLearningTracking();

    const handleTabChange = async (tabType, key) => {
        if (tabType === 'certifications' && certifications.length === 0) {
            dispatch(startHomePageLoader())
            await new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ payload: { pageId: 1, tabType, device: 'desktop'}, resolve, reject })));
            dispatch(stopHomePageLoader())
        }
        setKey(tabType)

        sendLearningTracking({
            productId: '',
            event: `homepage_popular_courses_${tabType}_tab_clicked`,
            pageTitle:`homepage_popular_${tabType}_courses`,
            sectionPlacement:'popular_courses',
            eventCategory: key,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: key,
        })
    }

    return (
        <section className="container mt-30 mb-0">
            <div className="row">
                <div className="col courses-tray popular-course-demand">
                    <h2 className="heading2 text-center mb-20">Popular courses in demand</h2>
                    <Tabs
                        id="controlled-tab-example"
                        activeKey={key}
                        onSelect={(tabType) => handleTabChange(tabType, key)}
                        className="category"
                    >

                        <Tab eventKey="master" title={<h2>Master’s</h2>}>
                            <MasterProduct tabType="master" popularProducts={courses} />
                        </Tab>
                        <Tab eventKey="certifications" title={<h2>Certifications</h2>}>
                            <CertificationProduct tabType="certifications" popularProducts={certifications} />
                        </Tab>

                    </Tabs>
                    {/* <span className="pink-circle1" data-aos="fade-right"></span> */}
                </div>
            </div>
        </section>
    );
}

export default PopularCourses;