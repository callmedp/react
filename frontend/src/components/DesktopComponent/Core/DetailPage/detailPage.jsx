import React, { useRef, useEffect } from 'react';
// import { Intersection } from 'react-use';
import Header from '../../Common/Header/header';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail from './Banner/banner';
import KeyFeatures from './KeyFeatures/keyFeatures';
import CourseOutline from './CourseOutline/courseOutline';
import CourseOutcome from './CourseOutcome/courseOutcome';
import SampleCertificate from './SampleCertificate/sampleCertificate';
import WhoLearn from './WhoLearn/whoLearn';
import TakeFreeTest from './TakeFreeTest/takeFreeTest';
import HowItWorks from './HowItWorks/howItWorks';
import SkillGain from './SkillGain/skillGain';
import OtherProviders from './OtherProviders/otherProviders';
import FAQ from './FAQ/faq';
import Reviews from './Reviews/Reviews';
import CoursesMayLike from './CoursesMayLike/coursesMayLike';
import EnquireNow from './EnquireNow/enquireNow';
import Footer from '../../Common/Footer/footer';
import '../SkillPage/skillPage.scss';
import Aos from "aos";
import "aos/dist/aos.css";

const DetailPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            <Header />
            <StickyNavDetail />
            <BannerCourseDetail/>
            <KeyFeatures />
            
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-12">
                        <CourseOutline />
                    </div>
                </div>
            </div>
            <div className="container-fluid mt-50 mb-50">
                <div className="row">
                    <div className="col-sm-9">
                        <CourseOutcome />
                    </div>
                    <div className="col-sm-3">
                        <SampleCertificate />
                    </div>
                </div>
            </div>
            <HowItWorks />
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-9">
                        <WhoLearn />
                    </div>
                    <div className="col-sm-3">
                        <TakeFreeTest />
                    </div>
                </div>
            </div>
            <SkillGain />
            <OtherProviders />
            <FAQ />
            <Reviews />
            <EnquireNow />
            <CoursesMayLike />
            <Footer />
        </div>
    )
}

export default DetailPage;