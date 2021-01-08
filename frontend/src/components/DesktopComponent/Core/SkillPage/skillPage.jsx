import React, { useState, useEffect } from 'react';
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
import queryString from 'query-string';
import { storageTrackingInfo, removeTrackingInfo, getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import Loader from '../../Common/Loader/loader';
import './skillPage.scss'
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { fetchPopularCourses } from 'store/Footer/actions/index';
import { useDispatch, useSelector } from 'react-redux';
import { zendeskTimeControlledWindow } from 'utils/zendeskIniti';
import Aos from "aos";
// import "aos/dist/aos.css";
import { Helmet } from 'react-helmet';

const SkillPage = (props) => {
    const pageId = props?.match?.params?.id;
    const dispatch = useDispatch();

    const { skillLoader } = useSelector(store => store.loader); 
    const { id } = useSelector( store => store.skillBanner );   
    const meta_tags = useSelector((store) => store.skillBanner.meta ? store.skillBanner.meta : '');
    const [ hasFaq, setHasFaq ] = useState(false)
    const [ hasLearnerStories, setHasLearnerStories ] = useState(false)
 

    const handleEffects = async () => {
        const {
            location: { search },
            history,
          } = props;
        const query = queryString.parse(search);
        if(query['t_id']) {
            query['prod_id'] = pageId;
            query['product_tracking_mapping_id'] = 10;
            storageTrackingInfo(query);
            dispatch(trackUser({
                "query" : query, 
                "action" : "skill_page"}));
        }else{
            let tracking_data = getTrackingInfo();
            if (tracking_data['prod_id'] != pageId && tracking_data['product_tracking_mapping_id'] == '10'){
                removeTrackingInfo()}
        }
        
        };

    useEffect(() => {
        
        handleEffects();
    
        if (!(window && window.config && window.config.isServerRendered)) {
            new Promise((resolve, reject) => dispatch(fetchSkillPageBanner({ id: pageId, 'medium': 0, resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchCoursesAndAssessments({ id: pageId, resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchDomainJobs({ id: pageId, resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchPopularCourses({ id: pageId, resolve, reject })))
        }
        else {
         
            delete window.config?.isServerRendered
        }
        //Zendesk Chat
        zendeskTimeControlledWindow(7000)
    }, [pageId])

    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            { skillLoader ? <Loader /> : ''}
            <Helmet>
                <title>{meta_tags.title}</title>
                <meta name="description" content={meta_tags.description} />
                <meta property="og:title" content={meta_tags.title} />
                <meta property="og:url" content={meta_tags._url} />
                <meta property="og:description" content={meta_tags.og_description} />
                <meta property="og:type" content={meta_tags.og_type} />
                <meta property="og:site_name" content={meta_tags.site_name} />
                <meta property="fb:profile_id" content={meta_tags.og_profile_id} />
                <meta itemProp="name" content={meta_tags.title} />
                <meta itemProp="url" content={meta_tags._url} />
                <meta itemProp="description" content={meta_tags.og_description} />
                <link rel="canonical" href={meta_tags._url} />
            </Helmet>
            <Header />
            <StickyNav hasFaq={hasFaq} hasLearnerStories={hasLearnerStories} />
            <SkillBanner />
            <section className="container">
                <div className="row">
                    <div className="col-sm-9">
                        <div className="ml-5">
                            <AboutSection />
                            <WhoLearn />
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
            <FAQ setHasFaq={setHasFaq} />
            <LearnersStories setHasLearnerStories={setHasLearnerStories} />
            <Footer />
        </div>
    )
}

export default SkillPage;