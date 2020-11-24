import React, { useRef } from 'react';
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
import './skillPage.scss'

const SkillPage = (props) => {

    const pageId = props.match.params.id;


    return (
        <div>
            <StickyNav  />
            <SkillBanner pageId={pageId}/>
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
            <CoursesTray pageId={pageId} />
            <OtherSkills />
            <section className="container">
                <aside className="row">
                    <div className="col">
                        <DomainJobs pageId={pageId}/>
                    </div>
                    <div className="col">
                        <WriteMyResume />
                    </div>
                </aside>
            </section>
            <WhyChooseUs />
            <FAQ  />
            <LearnersStories />
        </div>
    )
}

export default SkillPage;