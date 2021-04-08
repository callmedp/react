import React, { useEffect }from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import CourseDetailBanner1 from './Banner/Banner1';
import CourseEnrol1 from './CourseEnrol/courseEnroll1';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import WhatYouGet from './KeyFeatures/whatYouGet';
import HowItWorks from './HowItWorks/howItWorks1';
import TopicsCovered from './TopicsCovered/topicsCovered';
import Reviews from './Reviews/reviews';
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
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return(
        <div>
            <MenuNav />
            <header className="m-container m-header detail-bg">
                <Header />
                <CourseDetailBanner1 />
            </header>
            <main className="mb-0">
                <CourseEnrol1 />
                {/* <StickyNavDetail /> */}
                <WhatYouGet />
                <HowItWorks />
                <TopicsCovered />
                <Reviews />
                <CoursesMayLike />
                <CTA />
                {/* <EnquiryModal /> */}
                {/* <CertificateModal /> */}
                {/* <ReviewModal /> */}
            </main>
            <Footer />
        </div>

    )
}

export default DetailPage; 