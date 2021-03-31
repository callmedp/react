import React, { useEffect } from 'react';
import Header from '../../Common/Header/header';
import StickyNavDetail from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail from './Banner/banner';
import KeyFeatures from './KeyFeatures/keyFeatures';
import CourseOutline from './CourseOutline/courseOutline';
// import CourseOutcome from './CourseOutcome/courseOutcome';
// import SampleCertificate from './SampleCertificate/sampleCertificate';
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
import { fetchMainCourses } from 'store/DetailPage/actions';
import { useSelector, useDispatch } from 'react-redux';
import { startMainCourseLoader, stopMainCourseLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';

const DetailPage = (props) => {
    const dispatch = useDispatch();
    const {product_detail, skill} = useSelector(store => store?.mainCourses);
    const {match: {params: {id}}, history} = props;
    const { mainCourseLoader } = useSelector(store => store.loader);

    useEffect( () => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [id])

    const handleEffects = async () => {
        try {
            dispatch(startMainCourseLoader());
            await new Promise((resolve, reject) => dispatch(fetchMainCourses({ payload: {id: id?.split('-')[1] },resolve, reject })));
            dispatch(stopMainCourseLoader());
        }
        catch (error) {
            dispatch(stopMainCourseLoader());
            if (error?.status == 404) history.push('/404');
        }
        dispatch(stopMainCourseLoader());
    };

    return (
        <div>
            { mainCourseLoader ? <Loader /> : ''}
            <Header />
            <StickyNavDetail/>
            <BannerCourseDetail product_detail={product_detail}/>
            {product_detail?.prd_uget && <KeyFeatures prd_uget={product_detail?.prd_uget}/>}
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
            <Reviews id={id?.split('-')[1]} product_detail={product_detail}/>
            <EnquireNow {...props} />
            { skill && <CoursesMayLike product_id={id?.split('-')[1]} skill={skill}/> }
            <Footer />
        </div>
    )
}

export default DetailPage;