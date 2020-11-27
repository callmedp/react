import React, { useEffect } from 'react';
import React from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import SkillBanner from './Banner/Banner';
import BannerSlider from './BannerSlider/bannerSlider';
import PopularCourses from './PopularCourses/popularCourses';
import WhoLearn from './WhoLearn/whoLearn';
import SkillGain from './SkillGain/skillGain';
import LearnersStories from './LearnersStories/learnersStories';
import WriteMyResume from './WriteMyResume/writeMyResume';
import WhyChooseUs from './WhyChooseUs/whyChooseUs';
import OtherSkills from './OtherSkills/otherSkills';
import FAQ from './FAQ/faq';
import DomainJobs from './DomainJobs/domainJobs';
import { useDispatch } from 'react-redux';
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import Courses from './CoursesTray/Courses';
import Assessment from './CoursesTray/Assessment';
import '../SkillPage/skillPage.scss';


const SkillPage = (props) => {
    const dispatch = useDispatch()
    const pageId = props.match.params.id;
    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId, 'medium': 1}))
    },[])
    return(

        <section className="m-container-fluid mt-0 mb-0 pt-0">
            <div className="m-tabset">
                
                <input type="radio" name="tabset" id="tab1" aria-controls="about" checked />
                <label htmlFor="tab1">About</label>

                <input type="radio" name="tabset" id="tab2" aria-controls="courses" />
                <label htmlFor="tab2">Courses</label>

                <input type="radio" name="tabset" id="tab3" aria-controls="assessment" />
                <label htmlFor="tab3">Assessment</label>
                
                <div className="tab-panels">
                    <div id="about" className="tab-panel">
                        <PopularCourses />
                        <WhoLearn />
                        <SkillGain />
                        <LearnersStories />
                        <WriteMyResume />
                        <WhyChooseUs />
                        <OtherSkills />
                        <FAQ />
                        <DomainJobs />
                    </div>
                    <div id="courses" class="tab-panel">
                        <Courses />
                    </div>
                    <div id="assessment" class="tab-panel">
                        <Assessment />
                    </div>
                </div>
            </section>
            <Footer />
            <CTA />
        </main>

    )
}

export default SkillPage;