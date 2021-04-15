import React, { useEffect, useState } from 'react';
import Header from '../../Common/Header/header';
import StickyNav from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail from './Banner/banner';
import KeyFeatures from './KeyFeatures/keyFeatures';
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
import { fetchMainCourses } from 'store/DetailPage/actions';
import { useSelector, useDispatch } from 'react-redux';
import { startMainCourseLoader, stopMainCourseLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';
import MetaContent from "../../Common/MetaContent/metaContent";
import queryString from 'query-string';
import { getTrackingInfo, storageTrackingInfo, removeTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const DetailPage = (props) => {
    const dispatch = useDispatch();
    const {product_detail, skill, product_id, product_tracking_mapping_id} = useSelector(store => store?.mainCourses);
    const meta_tags = product_detail?.meta;
    const {location: { search }, match: {params: {id}}, history} = props;
    const { mainCourseLoader } = useSelector(store => store.loader);
    const [showStickyNav, setShowStickyNav] = useState(false);
    const [varChecked, changeChecked] = useState({});
    const [frqntProd, addFrqntProd] = useState([]);
    const completeDescription = (product_detail?.prd_about ? (product_detail?.prd_about + ' <br /> ') : '') + (product_detail?.prd_desc ? product_detail?.prd_desc : '')
    const reqLength = 250;

    useEffect( () => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        window.addEventListener('scroll', handleScroll);
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
              action: "ln_course_page",
            })
          );
        }
        else {
          let tracking_data = getTrackingInfo();
          if (tracking_data["prod_id"] != id.split('-')[1] && tracking_data["product_tracking_mapping_id"] === product_tracking_mapping_id) removeTrackingInfo();
        }
    };

    return (
        <div>
            { mainCourseLoader ? <Loader /> : ''}
            { meta_tags && <MetaContent meta_tags={meta_tags} /> }

            <Header />
            {
                    showStickyNav && <StickyNav 
                        outline={(product_detail?.chapter && product_detail?.prd_service !== 'assessment') ? true : false}
                        topics={(product_detail?.chapter && product_detail?.prd_service === 'assessment') ? true : false}
                        faq = {product_detail?.faq ? true : false}
                        product_detail={product_detail} prdId={id} varChecked={varChecked}
                        frqntProd={frqntProd} product_id={product_id}
                        />
            }
            <BannerCourseDetail 
                frqntProd={frqntProd}
                addFrqntProd={addFrqntProd}
                product_detail={product_detail}
                varChecked={varChecked}
                changeChecked={changeChecked}
                prdId={id} product_id={product_id}
                providerCount={product_detail?.pop_list?.length}
                completeDescription={completeDescription}
                reqLength={reqLength}
            />
            {product_detail?.prd_uget && <KeyFeatures prd_uget={product_detail?.prd_uget} pTF={product_detail?.pTF} prd_vendor_slug={product_detail?.prd_vendor_slug} />}
            
            {
                completeDescription?.length > reqLength ?  <AboutSection completeDescription={completeDescription} /> : ''
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
                (product_detail?.prd_should_lrn || !product_detail?.free_test) &&
                <div className="container-fluid">
                    <div className="row">
                        { 
                            product_detail?.prd_should_lrn && 
                            <div className="col-sm-9">
                                <WhoLearn prd_lrn_data={product_detail?.prd_should_lrn_dt}/> 
                            </div>
                        }
                        {
                            !product_detail?.free_test &&
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

            <Reviews id={id?.split('-')[1]} product_detail={product_detail} pUrl={props?.match?.url}/>

            <EnquireNow {...props} />
            
            { skill && <CoursesMayLike product_id={id?.split('-')[1]} skill={skill}/> }
            
            <Footer />
        </div>
    )
}

export default DetailPage;