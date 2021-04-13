import React, { useEffect, useState } from 'react';
import Header from '../../Common/Header/header';
import StickyNav from './StickyNavDetail/stickyNavDetail';
import BannerCourseDetail from './Banner/banner';
import KeyFeatures from './KeyFeatures/keyFeatures';
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

const DetailPage = (props) => {
    const dispatch = useDispatch();
    const {product_detail, skill} = useSelector(store => store?.mainCourses);
    const meta_tags = product_detail?.meta;
    const {match: {params: {id}}, history} = props;
    const { mainCourseLoader } = useSelector(store => store.loader);
    const [showStickyNav, setShowStickyNav] = useState(false);
    const [varChecked, changeChecked] = useState({});
    const [frqntProd, addFrqntProd] = useState([]);

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
                    new Promise((resolve, reject) => dispatch(fetchMainCourses({ payload: {id: id?.split('-')[1], device:'desktop' },resolve, reject })));
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
    };

    return (
        <div>
            { mainCourseLoader ? <Loader /> : ''}
            { meta_tags && <MetaContent meta_tags={meta_tags} /> }

            <Header />
            {
                    showStickyNav && <StickyNav 
                        outline={product_detail?.chapter ? true : false}
                        faq = {product_detail?.faq ? true : false}
                        product_detail={product_detail} prdId={id} varChecked={varChecked}
                        frqntProd={frqntProd}
                        />
            }
            <BannerCourseDetail frqntProd={frqntProd} addFrqntProd={addFrqntProd} product_detail={product_detail} varChecked={varChecked} changeChecked={changeChecked}/>
            {product_detail?.prd_uget && <KeyFeatures prd_uget={product_detail?.prd_uget} pTF={product_detail?.pTF} prd_vendor_slug={product_detail?.prd_vendor_slug} />}
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
            <Reviews id={id?.split('-')[1]} product_detail={product_detail} pUrl={props?.match?.url}/>
            <EnquireNow {...props} />
            { skill && <CoursesMayLike product_id={id?.split('-')[1]} skill={skill}/> }
            <Footer />
        </div>
    )
}

export default DetailPage;