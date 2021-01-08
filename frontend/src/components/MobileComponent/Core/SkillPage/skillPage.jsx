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
import queryString from 'query-string';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { trackUser } from 'store/Tracking/actions/index.js';
import { storageTrackingInfo, removeTrackingInfo, getTrackingInfo } from 'utils/storage.js';
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
import { fetchPopularCourses } from 'store/Footer/actions/index';
import Aos from "aos";
// import "aos/dist/aos.css";
import { Helmet } from 'react-helmet';
import { startSkillPageLoader, stopSkillPageLoader } from 'store/Loader/actions/index';

const SkillPage = (props) => {

    const dispatch = useDispatch();
    const { history } = props;
    const pageId = props.match.params.id;
    const [enquiryForm, setEnquiryForm] = useState(false);
    const [tabType, setTabType] = useState('about');
    const [showSearchPage, setShowSearchPage] = useState(false);
    const { skillLoader } = useSelector(store => store.loader);
    const { name } = useSelector(store => store.skillBanner);
    const meta_tags = useSelector((store) => store.skillBanner.meta ? store.skillBanner.meta : '');

    const handleEffects = async () => {

        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startSkillPageLoader());
                new Promise((resolve, reject) => dispatch(fetchCoursesAndAssessments({ id: pageId, 'medium': 1, resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchDomainJobs({ id: pageId, resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchRecommendedProducts({ resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchPopularCourses({ id: pageId, resolve, reject })))
                await new Promise((resolve, reject) => dispatch(fetchSkillPageBanner({ id: pageId, 'medium': 1, resolve, reject })))
                dispatch(stopSkillPageLoader());
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                history.push('/404');
            }
        }

        const { location: { search } } = props;
        const query = queryString.parse(search);
        if (!!query) {
            query['prod_id'] = pageId;
            query['product_tracking_mapping_id'] = 10;
            storageTrackingInfo(query);
            dispatch(trackUser({ "query": query, "action": "skill_page" }));
        }
        else {
            let tracking_data = getTrackingInfo();
            if (tracking_data['prod_id'] != pageId && tracking_data['product_tracking_mapping_id'] == '10') {
                removeTrackingInfo()
            }
        }

    };

    useEffect(() => {

        handleEffects();

    }, [pageId])

    useEffect(() => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <main className="m-container-fluid mt-0 pt-0">
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
            { showSearchPage ? <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header m-tabset-pos">
                        <Header setShowSearchPage={setShowSearchPage} />
                    </header>
                    <section className="m-tabset mt-0 mb-0 m-skill-ht-remove">
                        <StickyNav tabType={tabType} setTabType={setTabType} />
                        <div className="tab-panels">
                            {tabType === "about" ?
                                (
                                    <div id="about" className="tab-panel">
                                        <SkillBanner />
                                        <BannerSlider />
                                        <PopularCourses setTabType={setTabType} pageId={pageId} />
                                        <WhoLearn />
                                        <SkillGain />
                                        <LearnersStories />
                                        <WriteMyResume />
                                        <WhyChooseUs />
                                        <OtherSkills />
                                        <FAQ />
                                        <DomainJobs />
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
                    <CTA setEnquiryForm={setEnquiryForm} pageType='skill' heading={name} />
                    {
                        enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} /> : null
                    }
                </>
            }
        </main>
    )
}

export default SkillPage;