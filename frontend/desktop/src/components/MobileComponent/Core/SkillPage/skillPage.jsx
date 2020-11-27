import React, { useEffect } from 'react';
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
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import Courses from './CoursesTray/Courses';
import Assessment from './CoursesTray/Assessment';
import '../SkillPage/skillPage.scss';
import Footer from '../../Common/Footer/Footer';
import CTA from '../../Common/CTA/CTA';
import StickyNav from './StickyNav/stickyNav';


const SkillPage = (props) => {
    const dispatch = useDispatch()
    const pageId = props.match.params.id;
    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId, 'medium': 1}))
        dispatch(fetchCoursesAndAssessments({ id: pageId, 'medium': 1}));
    },[])
    return(
        <main className="m-container-fluid mt-0 pt-0">
            <MenuNav />
            <Header />
            <section class="m-tabset mt-0 mb-0 m-tabset-pos">
                <StickyNav />
                <div className="tab-panels">
                    <div id="about" className="tab-panel">
                        <SkillBanner />
                        <BannerSlider />
                        <PopularCourses />
                        <WhoLearn />
                        <SkillGain />
                        <LearnersStories />
                        <WriteMyResume />
                        <WhyChooseUs />
                        <OtherSkills />
                        <FAQ />
                        <DomainJobs pageId={pageId}/>
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