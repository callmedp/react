import React, { useRef, useEffect } from 'react';
// import { Intersection } from 'react-use';
import Header from '../../Common/Header/header';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail1 from './Banner/banner1';
import HowItWorks1 from './HowItWorks/howItWorks1';
import TopicsCovered from './TopicsCovered/topicsCovered';
import Reviews from './Reviews/Reviews';
import CoursesMayLike from './CoursesMayLike/coursesMayLike';
import EnquireNow from './EnquireNow/enquireNow';
import Footer from '../../Common/Footer/footer';
import '../SkillPage/skillPage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import WhatYouGet from './KeyFeatures/whatYouGet';

const DetailPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            <Header />
            <StickyNavDetail />
            <BannerCourseDetail1 />
            <WhatYouGet />
            <HowItWorks1 />
            <TopicsCovered />
            <Reviews />
            {/* <EnquireNow /> */}
            <CoursesMayLike />
            <Footer />
        </div>
    )
}

export default DetailPage; 