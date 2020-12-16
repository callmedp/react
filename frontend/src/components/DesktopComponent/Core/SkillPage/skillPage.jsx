import React, { useRef, useEffect } from 'react';
import SkillBanner from './Banner/banner';
import AboutSection from './AboutSection/aboutSection';
import WhoLearn from './WhoLearn/whoLearn';
import NeedHelp from './NeedHelp/needHelp';
import PopularCourses from './PopularCourses/popularCourses';
import SkillGain from './SkillGain/skillGain';
import CoursesTray from './CoursesTray/coursesTray';
import OtherSkills from './OtherSkills/otherSkills';
import DomainJobs from './DomainJobs/domainJobs';
import WriteMyResume from './WriteMyResume/writeMyResume';
import WhyChooseUs from './WhyChooseUs/whyChooseUs';
import FAQ from './FAQ/faq';
import LearnersStories from './LearnersStories/learnersStories';
import StickyNav from './StickyNav/stickyNav';
import Header from '../../Common/Header/header';
import Footer from '../../Common/Footer/footer';
import Loader from '../../Common/Loader/loader';
import './skillPage.scss'
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { useDispatch, useSelector } from 'react-redux';
import { zendeskTimeControlledWindow } from 'utils/zendeskIniti'

const SkillPage = (props) => {

    const pageId = props.match.params.id;
    const dispatch = useDispatch()
    
    const { skillLoader } = useSelector( store => store.loader );

    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId, 'medium': 0}));
        dispatch(fetchCoursesAndAssessments({ id: pageId }));
        dispatch(fetchDomainJobs({id : pageId}))
        //Zendesk Chat
        zendeskTimeControlledWindow(7000)
    },[pageId])

    return (
        <div>
            { skillLoader ? <Loader/> : '' }
            <Header/>
            <StickyNav  />
            <SkillBanner />
            <section className="container">
                <div className="row">
                    <div className="col-sm-9">
                        <div className="ml-5">
                            <AboutSection  />
                            <WhoLearn/>
                        </div>
                    </div>
                    <div className="col-sm-3 right-widget">
                        <NeedHelp />
                        <PopularCourses />
                    </div>
                </div>
            </section>
            <SkillGain />
            <CoursesTray />
            <OtherSkills />
            <section className="container">
                <aside className="row">
                    <div className="col">
                        <DomainJobs />
                    </div>
                    <div className="col">
                        <WriteMyResume />
                    </div>
                </aside>
            </section>
            <WhyChooseUs />
            <FAQ  />
            <LearnersStories />
            <Footer/>
        </div>
    )
}

export default SkillPage;