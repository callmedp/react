import React, { useEffect } from 'react';
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
import { fetchMainCourses } from 'store/DetailPage/actions';
import { useSelector, useDispatch } from 'react-redux';

const DetailPage = (props) => {
    const {product_detail, skill} = useSelector(store => store?.mainCourses);
    const dispatch = useDispatch();
    const {match: {params: {id}}} = props;


    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });

        handleEffects();
    }, [])

    const handleEffects = async () => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchMainCourses({ id: id.split('-')[1] ,resolve, reject })));
        }
        catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
            }
        }
    };

    return (
        <div>
            <Header />
            <StickyNavDetail/>
            <BannerCourseDetail product_detail={product_detail}/>
            <KeyFeatures prd_uget={product_detail?.prd_uget}/>
            
            {
                product_detail?.chapter && 
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-sm-12">
                            <CourseOutline chapter_list={product_detail?.chapter_list}/>
                        </div>
                    </div>
                </div>
            }
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
                       { product_detail?.prd_should_lrn && <WhoLearn prd_lrn_data={product_detail?.prd_should_lrn_dt}/> }
                    </div>
                    <div className="col-sm-3">
                        <TakeFreeTest should_take_test_url={product_detail?.shld_take_test_slg} />
                    </div>
                </div>
            </div>
            { skill && <SkillGain skill={skill}/> }
            { product_detail?.pop && <OtherProviders pop_list={product_detail?.pop_list} /> }
            { product_detail?.faq && <FAQ faq_list={product_detail?.faq_list}/> }
            <Reviews id={id?.split('-')[1]}/>
            <EnquireNow {...props} />
            <CoursesMayLike />
            <Footer />
        </div>
    )
}

export default DetailPage;