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
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import Courses from './CoursesTray/Courses';
import Assessment from './CoursesTray/Assessment';
import '../SkillPage/skillPage.scss';
import Footer from '../../Common/Footer/Footer';
import CTA from '../../Common/CTA/CTA';
import StickyNav from './StickyNav/stickyNav';
import EnquiryModal from '../../Common/Modals/EnquiryModal';
import Loader from '../../Common/Loader/loader';
import SearchPage from '../../Common/SearchPage/SearchPage';
import { fetchRecommendedProducts } from 'store/RecommendedCourses/actions/index';
import Aos from "aos";
// import "aos/dist/aos.css";


const SkillPage = (props) => {
   
  

    const dispatch = useDispatch()
    const pageId = props.match.params.id;
    const [enquiryForm, setEnquiryForm] = useState(false)
    const [tabType, setTabType] = useState('about')
    const [showSearchPage, setShowSearchPage] = useState(false)

    const { skillLoader } = useSelector( store => store.loader );
    const { name } = useSelector( store => store.skillBanner )

    useEffect(() => {

        if (!(window && window.config && window.config.isServerRendered)) {
            new Promise((resolve, reject) => dispatch(fetchSkillPageBanner({id : pageId, 'medium': 1, resolve, reject})))
            new Promise((resolve, reject) => dispatch(fetchCoursesAndAssessments({ id: pageId, 'medium': 1, resolve, reject})));
            new Promise((resolve, reject) => dispatch(fetchDomainJobs({id : pageId, resolve, reject})));
            new Promise((resolve, reject) => dispatch(fetchRecommendedProducts({resolve, reject})))
        }
        else {
            delete window.config?.isServerRendered
        }



    },[pageId])

    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return(
        <main className="m-container-fluid mt-0 pt-0">
            { skillLoader ? <Loader/> : '' }
            { showSearchPage ? <SearchPage setShowSearchPage={setShowSearchPage} />:
            <>
                <MenuNav />
                <header className="m-container m-header m-tabset-pos">
                    <Header setShowSearchPage={setShowSearchPage}/>
                </header>
                <section className="m-tabset mt-0 mb-0 m-skill-ht-remove">
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
                                    <DomainJobs/>
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
                    <Footer />
                </section>
                <CTA setEnquiryForm={setEnquiryForm} pageType='skill' heading={name}/>
                {
                    enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} /> : null
                }
            </>
            }
        </main>
    )
}

export default SkillPage;