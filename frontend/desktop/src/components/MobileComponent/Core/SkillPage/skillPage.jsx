import React, { useEffect } from 'react';
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
            <div class="m-tabset">
                
                <input type="radio" name="tabset" id="tab1" aria-controls="about" checked />
                <label for="tab1">About</label>

                <input type="radio" name="tabset" id="tab2" aria-controls="courses" />
                <label for="tab2">Courses</label>

                <input type="radio" name="tabset" id="tab3" aria-controls="assessment" />
                <label for="tab3">Assessment</label>
                
                <div class="tab-panels">
                    <div id="about" class="tab-panel">
                        <PopularCourses />
                        <WhoLearn />
                        <SkillGain />
                        <LearnersStories />
                        <WriteMyResume />
                        <WhyChooseUs />
                        <OtherSkills />
                        <FAQ />
                        <DomainJobs pageId={pageId} />
                    </div>
                    <div id="courses" class="tab-panel">
                        <Courses />
                    </div>
                    <div id="assessment" class="tab-panel">
                        <Assessment />
                    </div>
                </div>
                
            </div>
        </section>

    )
}

export default SkillPage;