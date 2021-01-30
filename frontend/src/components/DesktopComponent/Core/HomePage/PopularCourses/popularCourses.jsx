import React, {useState} from 'react';
import '../../SkillPage/CoursesTray/coursesTray.scss';
import './popularCourses.scss'
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import MasterProduct from './HomeProduct/homeProduct';
import CertificationProduct from './HomeProduct/homeProduct';
   
function PopularCourses() {
  const [key, setKey] = useState('categories1');

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
                    <MasterProduct/>
                </Tab>
                <Tab eventKey="categories2" title={<h2>Certifications</h2>}>
                    <CertificationProduct/>
                </Tab>
                
                </Tabs>
                <span className="pink-circle1" data-aos="fade-right"></span>
            </div>
        </div>
    </section>
  );
}
   
export default PopularCourses;