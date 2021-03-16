import React, { useState, useEffect } from 'react';
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

const DetailPage = (props) => {

    const [reviewModal, showReviewModal] = useState(false)

    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return(
        <div>
            <MenuNav />
            {
                reviewModal ? <ReviewModal showReviewModal={showReviewModal}/> :<>
                <header className="m-container m-header detail-bg">
                <Header />
                <CourseDetailBanner />
            </header>
            <main className="mb-0">
                <CourseEnrol />
                {/* <StickyNavDetail /> */}
                <KeyFeatures />
                <CourseOutline />
                <CourseOutcome />
                <SampleCertificate />
                <HowItWorks />
                <WhoLearn />
                <SkillGain />
                <TakeFreeTest />
                <OtherProviders />
                <FAQ />
                <Reviews showReviewModal={showReviewModal}/>
                <CoursesMayLike />
                <CTA />
                {/* <EnquiryModal /> */}
                {/* <CertificateModal /> */}
            </main>
            <Footer /></>
            }
        </div>

    )
}

export default DetailPage;