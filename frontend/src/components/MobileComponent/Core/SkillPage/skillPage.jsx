import React, { useEffect, useState } from 'react';
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
import { useDispatch, useSelector } from 'react-redux';
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import Courses from './CoursesTray/Courses';
import Assessment from './CoursesTray/Assessment';
import '../SkillPage/skillPage.scss';
import Footer from '../../Common/Footer/Footer';
import CTA from '../../Common/CTA/CTA';
import StickyNav from './StickyNav/stickyNav';
import EnquiryModal from '../../Common/Modals/EnquiryModal';
import Loader from '../../Common/Loader/loader';
import SearchPage from '../../Common/SearchPage/SearchPage';


const SkillPage = (props) => {
    const dispatch = useDispatch()
    const pageId = props.match.params.id;
    const [enquiryForm, setEnquiryForm] = useState(false)
    const [tabType, setTabType] = useState('about')
    const [showSearchPage, setShowSearchPage] = useState(false)

    const { skillLoader } = useSelector( store => store.loader );

    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId, 'medium': 1}))
        dispatch(fetchCoursesAndAssessments({ id: pageId, 'medium': 1}));
    },[pageId])

    return(
        <main className="m-container-fluid mt-0 pt-0">
            { skillLoader ? <Loader/> : '' }
            { showSearchPage ? <SearchPage />:
            <>
                <MenuNav />
                <header className="m-container m-header m-tabset-pos">
                    <Header setShowSearchPage={setShowSearchPage}/>
                </header>
                <section class="m-tabset mt-0 mb-0 m-skill-ht-remove">
                    <StickyNav tabType={tabType} setTabType={setTabType} />
                    <div className="tab-panels">
                        { tabType === "about" ? 
                            (
                                <div id="about" className="tab-panel">
                                    <SkillBanner />
                                    <BannerSlider />
                                    <PopularCourses setTabType={setTabType} />
                                    <WhoLearn />
                                    <SkillGain />
                                    <LearnersStories />
                                    <WriteMyResume />
                                    <WhyChooseUs />
                                    <OtherSkills />
                                    <FAQ />
                                    <DomainJobs pageId={pageId}/>
                                </div>
                            ) :
                            tabType === 'courses' ? 
                            (
                                <div id="courses" className="tab-panel">
                                    <Courses />
                                </div>
                            ) :
                            (
                                <div id="assessment" className="tab-panel">
                                    <Assessment />
                                </div>
                            )
                            }
                    </div>
                </section>
                <Footer />
                <CTA setEnquiryForm={setEnquiryForm}/>
                {
                    enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} /> : null
                }
            </>
            }
        </main>
    )
}

export default SkillPage;