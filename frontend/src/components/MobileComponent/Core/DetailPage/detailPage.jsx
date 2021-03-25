import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import CourseDetailBanner from './Banner/Banner';
import CourseEnrol from './CourseEnrol/courseEnrol';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import KeyFeatures from './KeyFeatures/keyFeatures';
import CourseOutline from './CourseOutline/courseOutline';
import CourseOutcome from './CourseOutcome/courseOutcome';
import SampleCertificate from './SampleCertificate/sampleCertificate';
import HowItWorks from './HowItWorks/howItWorks';
import WhoLearn from './WhoLearn/whoLearn';
import SkillGain from './SkillGain/skillGain';
import TakeFreeTest from './TakeFreeTest/takeFreeTest';
import OtherProviders from './OtherProviders/otherProviders';
import Reviews from './Reviews/reviews';
import FAQ from './FAQ/faq';
import CoursesMayLike from './CoursesMayLike/coursesMayLike';
import Footer from '../../Common/Footer/Footer';
import CTA from '../../Common/CTA/CTA';
import CertificateModal from '../../Common/Modals/CertificateModal';
import EnquiryModal from '../../Common/Modals/EnquiryModal';
import ReviewModal from '../../Common/Modals/ReviewModal';
import '../DetailPage/detailPage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import { fetchRecommendedCourses, fetchReviews, fetchOtherProviderCourses, fetchMainCourses } from 'store/DetailPage/actions';

const DetailPage = (props) => {

    const [reviewModal, showReviewModal] = useState(false)
    const prdId = props.match.params.id;
    const dispatch = useDispatch()
    const { product_detail, skill } = useSelector(store => store?.mainCourses);
    const [enquiryForm, setEnquiryForm] = useState(false);
    const [varChecked, changeChecked] = useState({});

    console.log(product_detail)

    const handleEffects = async () => {
        try {
            if (!(window && window.config && window.config.isServerRendered)) {
                new Promise((resolve, reject) => dispatch(fetchMainCourses({ id: prdId?.split('-')[1] ,resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchReviews({ payload: { prdId: prdId?.split('-')[1] }, resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchRecommendedCourses({ resolve, reject })));
                await new Promise((resolve, reject) => dispatch(fetchOtherProviderCourses({ resolve, reject })));
            }
            else {
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
                console.log(error)
            }
        }

    };

    useEffect( () => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [prdId])

    return(
        <div>
            <MenuNav />
            {
                reviewModal ? <ReviewModal showReviewModal={showReviewModal} prdId={prdId}/> :<>
                <header className="m-container m-header detail-bg">
                <Header />
                <CourseDetailBanner product_detail={product_detail} prdId={prdId} varChecked={varChecked}/>
            </header>
            <main className="mb-0">
                <CourseEnrol product_detail={product_detail} varChecked={varChecked} changeChecked={changeChecked}/>
                {/* <StickyNavDetail /> */}
                <KeyFeatures prd_uget={product_detail?.prd_uget}/>
                {
                    product_detail?.chapter && 
                        <CourseOutline chapter_list={product_detail?.chapter_list}/>
                }
                {/* <CourseOutcome />
                <SampleCertificate /> */}
                <HowItWorks steps={product_detail?.dlvry_flow}/>
                { 
                    product_detail?.prd_should_lrn &&
                        <WhoLearn prd_lrn_data={product_detail?.prd_should_lrn_dt} />
                }
                { skill && <SkillGain skills={skill}/> }
                { product_detail?.free_test && <TakeFreeTest should_take_test_url={product_detail?.shld_take_test_slg} test_title={product_detail?.test_title} /> }
                <OtherProviders />
                { product_detail?.faq && <FAQ faq_list={product_detail?.faq_list}/> }
                <Reviews showReviewModal={showReviewModal} prdId={prdId}/>
                <CoursesMayLike />
                <CTA setEnquiryForm={setEnquiryForm} />
                {
                    enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} page="detailPage"/> : null
                }
                {/* <CertificateModal /> */}
            </main>
            <Footer /></>
            }
        </div>

    )
}

export default DetailPage;