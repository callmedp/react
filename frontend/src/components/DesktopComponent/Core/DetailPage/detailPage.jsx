import React, { useEffect, useState } from 'react';
import Header from '../../Common/Header/header';
import StickyNav from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail from './Banner/banner';
import KeyFeatures from './KeyFeatures/keyFeatures';
import WhatYouGet from './KeyFeatures/whatYouGet';
import AboutSection from './AboutSection/aboutSection';
import CourseOutline from './CourseOutline/courseOutline';
// import CourseOutcome from './CourseOutcome/courseOutcome';
// import SampleCertificate from './SampleCertificate/sampleCertificate';
import WhoLearn from './WhoLearn/whoLearn';
import TakeFreeTest from './TakeFreeTest/takeFreeTest';
import HowItWorks from './HowItWorks/howItWorks';
import TopicsCovered from './TopicsCovered/topicsCovered';
import SkillGain from './SkillGain/skillGain';
import OtherProviders from './OtherProviders/otherProviders';
import FAQ from './FAQ/faq';
import Reviews from './Reviews/Reviews';
import CoursesMayLike from './CoursesMayLike/coursesMayLike';
import EnquireNow from './EnquireNow/enquireNow';
import Footer from '../../Common/Footer/footer';
import '../SkillPage/skillPage.scss';
import Aos from "aos";
import { fetchMainCourses, fetchProductReviews } from 'store/DetailPage/actions';
import { useSelector, useDispatch } from 'react-redux';
import { startMainCourseLoader, stopMainCourseLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';
import MetaContent from "../../Common/MetaContent/metaContent";
import queryString from 'query-string';
import { getTrackingInfo, storageTrackingInfo, removeTrackingInfo, getCandidateId } from 'utils/storage.js';
import { chatbot_links } from 'utils/constants.js';
import { siteDomain } from 'utils/domains.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import ReviewModal from '../../Common/Modals/reviewModal';
import VideoModal from '../../Common/Modals/videoModal';
import { Helmet } from "react-helmet";

const DetailPage = (props) => {
    const dispatch = useDispatch();
    const {product_detail, skill, product_id, product_tracking_mapping_id, providerLength, ggn_contact_full } = useSelector(store => store?.mainCourses);
    const { prd_review_list, prd_rv_current_page, prd_rv_has_next } = useSelector( store => store.reviews );
    const meta_tags = product_detail?.meta;
    const {location: { search }, match: {params: {id}}, history} = props;
    const { mainCourseLoader } = useSelector(store => store.loader);
    const [showStickyNav, setShowStickyNav] = useState(false);
    const [varChecked, changeChecked] = useState({});
    const [frqntProd, addFrqntProd] = useState([]);
    const completeDescription = ((product_detail?.prd_about && (product_detail?.prd_about !== product_detail?.prd_desc)) 
                                    ? (product_detail?.prd_about + ' <br /> ') : '') + (product_detail?.prd_desc ? product_detail?.prd_desc : '')
    const reqLength = 250;
    const [detReviewModal, showReviewModal] = useState(false);
    const [videoModal, setVideoModal] = useState(false);
    const params = new URLSearchParams(props.location.search);
    const showAfterLoginReviewModal = params.get('sm');
    let currentPage = 1;

    // for chatbot details
    window["name"] = localStorage.getItem('userName') ? localStorage.getItem('userName') : 'Customer';
    window['candidate_id'] = localStorage.getItem('candidateId');
    window["course_name"] = product_detail?.prd_H1;
    window["contact_number_support"] = ggn_contact_full;
    window["link_interview_service"] = chatbot_links.link_interview_service;
    window["link_profile_booster"] = chatbot_links.link_profile_booster;
    window["link_resume_builder"] = chatbot_links.link_resume_builder;
    window["link_resume_writer"] = chatbot_links.link_resume_writer;
    window["candidate_id"] = localStorage.getItem('candidateId');
    window["link_payment"] = siteDomain+"/cart/payment-summary/?prod_id=" + product_id;

    useEffect( () => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        window.addEventListener('scroll', handleScroll);
        if(getCandidateId() && (showAfterLoginReviewModal === 'true')) showReviewModal(true)
        else showReviewModal(false)
    }, [id])

    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 300 ) {
            setShowStickyNav(true);
        }
        else setShowStickyNav(false);
    }

    const handleEffects = async () => {
        dispatch(startMainCourseLoader());
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                // dispatch(startMainCourseLoader());
                await new Promise((resolve, reject) => dispatch(fetchMainCourses({ payload: {id: id?.split('-')[1], device:'desktop' },resolve, reject })));
                dispatch(stopMainCourseLoader());
            }
            else {
                delete window.config?.isServerRendered;
                dispatch(stopMainCourseLoader());
            }

            await new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: id?.split('-')[1], page: currentPage, device: 'desktop' }, resolve, reject })));
        }
        catch (error) {
            dispatch(stopMainCourseLoader());
            if (error?.status == 404) history.push('/404');
        }
        dispatch(stopMainCourseLoader());

        const query = queryString.parse(search);
        if (query["t_id"]) {
          query["prod_id"] = id.split('-')[1];
          query["product_tracking_mapping_id"] = product_tracking_mapping_id;
          storageTrackingInfo(query);
          dispatch(
            trackUser({
              query: query,
              action: "product_page",
            })
          );
        }
        else {
          let tracking_data = getTrackingInfo();
          if (tracking_data["prod_id"] != id.split('-')[1] && tracking_data["product_tracking_mapping_id"] === product_tracking_mapping_id) removeTrackingInfo();
        }
    };

    return (
        <div itemScope itemType="http://schema.org/Product">
            <Helmet
            script={[
                { "src": (localStorage.getItem('script_link') ? localStorage.getItem('script_link') : null), "type": "text/javascript" }
            ]}
            />
            { mainCourseLoader ? <Loader /> : ''}
            { meta_tags && <MetaContent meta_tags={meta_tags} /> }

            {/* Review Modal */}
            {
                detReviewModal ? <ReviewModal detReviewModal={detReviewModal} prdId={id?.split('-')[1]} showReviewModal={showReviewModal} review={product_detail?.review} user_reviews={product_detail?.user_reviews} /> : ""
            }

            {   
                videoModal ? <VideoModal videoModal={videoModal}  setVideoModal={setVideoModal} videoUrl={product_detail?.prd_video} productName={product_detail?.prd_H1} /> : ""
            }

            <Header />

            {
                    showStickyNav && <StickyNav 
                        outline={(product_detail?.chapter && product_detail?.prd_service !== 'assessment') ? true : false}
                        topics={(product_detail?.chapter && product_detail?.prd_service === 'assessment') ? true : false}
                        faq = {product_detail?.faq ? true : false}
                        product_detail={product_detail} prdId={id} varChecked={varChecked}
                        frqntProd={frqntProd} product_id={product_id}
                        hasReview = { prd_review_list?.length ? true : false }
                        hasKeyFeatures = {product_detail?.prd_uget ? true : false}
                        hasWhatYouGet = {product_detail?.pTF === 16 ? true : false}
                        />
            }

            <BannerCourseDetail 
                frqntProd={frqntProd}
                addFrqntProd={addFrqntProd}
                product_detail={product_detail}
                varChecked={varChecked}
                changeChecked={changeChecked}
                product_id={product_id}
                providerCount={providerLength}
                completeDescription={completeDescription}
                reqLength={reqLength}
                showReviewModal={showReviewModal}
                setVideoModal={setVideoModal}
                pUrl={props?.match?.url}
                prd_review_list={prd_review_list}
                prd_product={product_detail?.prd_product}
                upc={product_detail?.pUPC}
            />

            { product_detail?.prd_uget && <KeyFeatures prd_uget={product_detail?.prd_uget} /> }

            { product_detail?.pTF === 16 && <WhatYouGet prd_vendor_slug={product_detail?.prd_vendor_slug} /> }
            
            {
                completeDescription?.length > reqLength ?  <AboutSection product_detail={product_detail} /> : ''
            }
            
            {
                 (product_detail?.chapter && product_detail?.prd_service !== 'assessment') && 
                 <div className="container-fluid">
                     <div className="row">
                         <div className="col-sm-12">
                             <CourseOutline chapter_list={product_detail?.chapter_list}/>
                         </div>
                     </div>
                 </div>
            }

            {/* commented due to lack of data */}
            {/* <div className="container-fluid mt-50 mb-50">
            <div className="row">
                <div className="col-sm-9">
                    <CourseOutcome />
                </div>
                <div className="col-sm-3">
                    <SampleCertificate />
                </div>
            </div>
            </div> */}

            { product_detail?.dlvry_flow && <HowItWorks dlvry_flow={product_detail?.dlvry_flow} /> }

            { (product_detail?.chapter && product_detail?.prd_service === 'assessment') && <TopicsCovered  chapter_list={product_detail?.chapter_list}/> }

            {
                (product_detail?.prd_should_lrn || product_detail?.free_test) &&
                <div className="container-fluid">
                    <div className="row">
                        { 
                            product_detail?.prd_should_lrn && 
                            <div className="col-sm-9">
                                <WhoLearn prd_lrn_data={product_detail?.prd_should_lrn_dt}/> 
                            </div>
                        }
                        {
                            product_detail?.free_test &&
                            <div className="col-sm-3">
                                <TakeFreeTest should_take_test_url={product_detail?.shld_take_test_slg} />
                            </div>
                        }
                    </div>
                </div>
            }

            { skill && skill.length > 0 && <SkillGain skill={skill}/> }

            { product_detail?.pop && <OtherProviders pop_list={product_detail?.pop_list} /> }
            
            { product_detail?.faq && <FAQ faq_list={product_detail?.faq_list}/> }

            {(prd_review_list && prd_review_list?.length) > 0 && <Reviews id={id?.split('-')[1]} product_detail={product_detail} pUrl={props?.match?.url} showReviewModal={showReviewModal} prd_review_list={prd_review_list} prd_rv_current_page={prd_rv_current_page} prd_rv_has_next={prd_rv_has_next} /> }
            
            <EnquireNow {...props} />
            
            { skill && <CoursesMayLike product_id={id?.split('-')[1]} skill={skill}/> }
            
            <Footer />
        </div>
    )
}

export default DetailPage;