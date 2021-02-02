import React, {useState} from 'react';
import '../../SkillPage/CoursesTray/coursesTray.scss';
import './popularCourses.scss'
import { Tabs, Tab } from 'react-bootstrap';
import MasterProduct from './HomeProduct/homeProduct';
import CertificationProduct from './HomeProduct/homeProduct';
import { useSelector } from 'react-redux';   

function PopularCourses() {
  const [key, setKey] = useState('categories1');

  const { courses, certifications } = useSelector( store => store.inDemand )

  return (
    <section className="container mt-30 mb-0">
        <div className="row"> 
            <div className="col courses-tray popular-course-demand">
                <h2 className="heading2 text-center mb-20">Popular courses in demand</h2>
                <Tabs
                id="controlled-tab-example"
                activeKey={key}
                onSelect={(k) => setKey(k)}
                className="category"
                >
        
                <Tab eventKey="categories1" title={<h2>Master’s</h2>}>
                    <MasterProduct tabType="master" popularProducts={courses} />
                </Tab>
                <Tab eventKey="categories2" title={<h2>Certifications</h2>}>
                    <CertificationProduct tabType="certification" popularProducts={certifications} />
                </Tab>
                
                </Tabs>
                <span className="pink-circle1" data-aos="fade-right"></span>
            </div>
        </div>
    </section>
  );
}
   
export default PopularCourses;