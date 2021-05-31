import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import CourseDetailBanner from './Banner/Banner';
import CourseEnrol from './CourseEnrol/courseEnrol';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import KeyFeatures from './KeyFeatures/keyFeatures';
import WhatYouGet from './KeyFeatures/whatYouGet';
import CourseOutline from './CourseOutline/courseOutline';
// import CourseOutcome from './CourseOutcome/courseOutcome';
// import SampleCertificate from './SampleCertificate/sampleCertificate';
import HowItWorks from './HowItWorks/howItWorks';
import TopicsCovered from './TopicsCovered/topicsCovered';
import WhoLearn from './WhoLearn/whoLearn';
import SkillGain from './SkillGain/skillGain';
import TakeFreeTest from './TakeFreeTest/takeFreeTest';
import OtherProviders from './OtherProviders/otherProviders';
import Reviews from './Reviews/reviews';
import FAQ from './FAQ/faq';
import CoursesMayLike from './CoursesMayLike/coursesMayLike';
import ComboIncludes from './ComboIncludes/comboIncludes';
import FrequentlyBought from './FrequentlyBought/frequentlyBought';
import Footer from '../../Common/Footer/Footer';
import CTA from '../../Common/CTA/CTA';
// import CertificateModal from '../../Common/Modals/CertificateModal';
import EnquiryModal from '../../Common/Modals/EnquiryModal';
import ReviewModal from '../../Common/Modals/ReviewModal';
import VideoModal from '../../Common/Modals/videoModal';
import '../DetailPage/detailPage.scss';
import Aos from "aos";
import MetaContent from '../../Common/MetaContent/metaContent';
import { fetchProductReviews, fetchMainCourses } from 'store/DetailPage/actions';
import SearchPage from '../../Common/SearchPage/SearchPage';
import { startMainCourseLoader, stopMainCourseLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';
import queryString from 'query-string';
import { getTrackingInfo, storageTrackingInfo, removeTrackingInfo, getCandidateId } from 'utils/storage.js';
import { chatbot_links } from 'utils/constants.js';
import { siteDomain } from 'utils/domains.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import About from '../DetailPage/About/aboutSection';

const DetailPage = (props) => {
    const { location: { search }, history } = props;
    const dispatch = useDispatch();
    const { mainCourseLoader } = useSelector(store => store.loader);
    const [reviewModal, showReviewModal] = useState(false)
    const prdId = props.match.params.id;
    const { product_detail, skill, ggn_contact, product_id, product_tracking_mapping_id, providerLength, ggn_contact_full } = useSelector(store => store?.mainCourses);
    const meta_tags = product_detail?.meta;
    const [enquiryForm, setEnquiryForm] = useState(false);
    const [videoModal, setVideoModal] = useState(false);
    const [varChecked, changeChecked] = useState({});
    const [showStickyNav, setShowStickyNav] = useState(false);
    const [showSearchPage, setShowSearchPage] = useState(false)
    const [frqntProd, addFrqntProd] = useState([]);
    const params = new URLSearchParams(props.location.search);
    const showAfterLoginReviewModal = params.get('sm');
    const { prd_review_list, prd_rv_total } = useSelector(store => store.reviews);
    const completeDescription = ((product_detail?.prd_about && (product_detail?.prd_about !== product_detail?.prd_desc)) ? (product_detail?.prd_about + ' <br /> ') : '') + (product_detail?.prd_desc ? product_detail?.prd_desc : '')
    const noOfWords = 250;

    // for chatbot
    window["name"] = localStorage.getItem('userName') ? localStorage.getItem('userName') : 'Customer';
    window["course_name"] = product_detail?.prd_H1;
    window["contact_number_support"] = ggn_contact_full;
    window["link_interview_service"] = chatbot_links.link_interview_service;
    window["link_profile_booster"] = chatbot_links.link_profile_booster;
    window["link_resume_builder"] = chatbot_links.link_resume_builder;
    window["link_resume_writer"] = chatbot_links.link_resume_writer;
    window["candidate_id"] = localStorage.getItem('candidateId');
    window["link_payment"] = siteDomain+"/cart/payment-summary/?prod_id=" + product_id;

    const handleEffects = async () => {

        try {
            dispatch(startMainCourseLoader());

            if (!(window && window.config && window.config.isServerRendered)) {
                await new Promise((resolve, reject) => dispatch(fetchMainCourses({ payload: { id: prdId?.split('-')[1], device: 'mobile' }, resolve, reject })));

                dispatch(stopMainCourseLoader());
            }
            else {
                dispatch(stopMainCourseLoader());
                delete window.config?.isServerRendered;
            }

            await new Promise((resolve, reject) => dispatch(fetchProductReviews({ payload: { prdId: prdId?.split('-')[1], page: 1, device: 'mobile' }, resolve, reject })));
        }
        catch (error) {
            dispatch(stopMainCourseLoader());

            if (error?.status == 404) {
                history.push('/404');
                console.log(error)
            }
        }

        const query = queryString.parse(search);
        if (query["t_id"]) {
            query["prod_id"] = prdId?.split('-')[1];
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
            if (tracking_data["prod_id"] != prdId?.split('-')[1] && tracking_data["product_tracking_mapping_id"] === product_tracking_mapping_id) removeTrackingInfo();
        }

        const scriptTag = document.createElement('script');

        scriptTag.src = localStorage.getItem('script_link');
        scriptTag.async = true;

        // console.log(scriptTag.toString())

        document.body.appendChild(scriptTag);
    };

    const getProductPrice = (product) => {
        let price = 0;
        price += frqntProd.reduce((previousValue, currentValue) => {
            return parseFloat(previousValue) + parseFloat(currentValue.inr_price);
        }, 0);
        return parseFloat(product) + price;
    };


    window["course_fee"] = getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb);

    const handleScroll = () => {
        const offset = window.scrollY;
        if (offset > 670) {
            setShowStickyNav(true);
        }
        else setShowStickyNav(false);
    }

    useEffect(() => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        window.addEventListener('scroll', handleScroll);
        if (getCandidateId() && (showAfterLoginReviewModal === 'true')) showReviewModal(true)
        else showReviewModal(false)
    }, [prdId])

    return(
        <div itemScope itemType="http://schema.org/Product">
            { mainCourseLoader ? <Loader /> : ''}

            { meta_tags && <MetaContent meta_tags={meta_tags} />}
            {
                showSearchPage ?
                    <SearchPage setShowSearchPage={setShowSearchPage} /> :
                    <>
                        <MenuNav />

                        <>
                            <header className="m-container m-header detail-bg">
                                <Header setShowSearchPage={setShowSearchPage} hideName={true} />
                                <CourseDetailBanner
                                    product_detail={product_detail}
                                    prdId={prdId}
                                    varChecked={varChecked}
                                    showReviewModal={showReviewModal}
                                    providerCount={providerLength}
                                    pUrl={props?.match?.url}
                                    prd_review_list={prd_review_list}
                                    completeDescription={completeDescription}
                                    noOfWords={noOfWords}
                                    setVideoModal={setVideoModal}
                                />
                            </header>
                            <main className="mb-0">
                                <CourseEnrol product_detail={product_detail} getProductPrice={getProductPrice} frqntProd={frqntProd} varChecked={varChecked} changeChecked={changeChecked} product_id={product_id} />
                                {
                                    showStickyNav && <StickyNavDetail
                                        outline={(product_detail?.chapter && product_detail?.prd_service !== 'assessment') ? true : false}
                                        topics={(product_detail?.chapter && product_detail?.prd_service === 'assessment') ? true : false}
                                        faq={product_detail?.faq ? true : false}
                                        product_detail={product_detail} prdId={prdId} varChecked={varChecked}
                                        frqntProd={frqntProd} product_id={product_id} prd_review_list={prd_review_list}
                                        hasKeyFeatures={product_detail?.prd_uget ? true : false}
                                        hasWhatYouGet={product_detail?.pTF === 16 ? true : false}
                                    />
                                }
                                {
                                    product_detail?.combo && <ComboIncludes comboList={product_detail.combo_list} />
                                }
                                {
                                    product_detail?.fbt && <FrequentlyBought fbtList={product_detail.fbt_list} addFrqntProd={addFrqntProd} frqntProd={frqntProd} />
                                }
                                {
                                    (product_detail?.prd_desc && completeDescription?.length > noOfWords) && <About desc={product_detail?.prd_desc} />
                                }
                                {
                                    product_detail?.prd_uget && <KeyFeatures prd_uget={product_detail?.prd_uget} />
                                }
                                {
                                    product_detail?.pTF === 16 && <WhatYouGet prd_vendor_slug={product_detail?.prd_vendor_slug} />
                                }

                                {
                                    (product_detail?.chapter && product_detail?.prd_service !== 'assessment') &&
                                    <CourseOutline chapter_list={product_detail?.chapter_list} />
                                }
                                {/* <CourseOutcome />
                                <SampleCertificate /> */}
                                <HowItWorks steps={product_detail?.dlvry_flow} />
                                {
                                    (product_detail?.chapter && product_detail?.prd_service === 'assessment') && <TopicsCovered chapter_list={product_detail?.chapter_list} />
                                }
                                {
                                    product_detail?.prd_should_lrn &&
                                    <WhoLearn prd_lrn_data={product_detail?.prd_should_lrn_dt} />
                                }
                                {skill?.length > 0 && <SkillGain skills={skill} />}
                                {product_detail?.free_test && <TakeFreeTest should_take_test_url={product_detail?.shld_take_test_slg} test_title={product_detail?.test_title} />}
                                {product_detail?.pop && <OtherProviders pop_list={product_detail?.pop_list} />}
                                {product_detail?.faq && <FAQ faq_list={product_detail?.faq_list} />}

                                {(prd_review_list && prd_review_list?.length) > 0 && <Reviews showReviewModal={showReviewModal} product_detail={product_detail} prdId={prdId} pUrl={props?.match?.url} prd_review_list={prd_review_list} prd_rv_total={prd_rv_total} />}

                                {skill?.length > 0 && <CoursesMayLike product_id={prdId} skill={skill} />}
                                <CTA setEnquiryForm={setEnquiryForm} contact={ggn_contact} />
                                {
                                    enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} page="detailPage" /> : null
                                }
                                {/* <CertificateModal /> */}
                                {reviewModal ? <ReviewModal showReviewModal={showReviewModal} prdId={prdId} product_detail={product_detail} review={product_detail?.review} /> : ""}

                                {videoModal ? <VideoModal setVideoModal = {setVideoModal} videoUrl = {product_detail?.prd_video} productName={product_detail?.prd_H1} />: '' }
                                 
                    </main>
                    <Footer pageType={"homePage"} /></>
                        </>
            }
                    </div>
    )
}

export default DetailPage;