import React, { useEffect, useState } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import { Link as LinkScroll } from 'react-scroll';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAddToCartEnroll, fetchAddToCartRedeem } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';
import { siteDomain } from 'utils/domains';
import { getStudyMode } from 'utils/detailPageUtils/studyMode';
import { getStudyLevel } from 'utils/detailPageUtils/studyLevel';
import ComboIncludes from '../ComboIncludes/comboIncludes';
import FrequentlyBought from '../FrequentlyBought/frequentlyBought';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { Toast } from '../../../Common/Toast/toast';

const BannerCourseDetail = (props) => {
    const {product_detail, varChecked, changeChecked, frqntProd, addFrqntProd, prdId, product_id, providerCount} = props;
    const reqLength = 365;
    // const inputCheckbox = useRef(null);
    // const regex = /<(.|\n)*?>/g;
    const [discountPrice, discountPriceSelected] = useState(0);
    const dispatch = useDispatch();
    const { mainCourseCartLoader } = useSelector(store => store.loader);
    const tracking_data = getTrackingInfo();
    const [readAll, setReadAll] = useState(false)

    const completeDescription = (product_detail?.prd_about || product_detail?.prd_desc) ? product_detail?.prd_about + ' <br /> ' + product_detail?.prd_desc : '';

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+' 
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    useEffect(() => {
        setReadAll(false)
    }, [prdId])

    const changeMode = (objj) => {
        let selectedObj = objj;
        discountPriceSelected(objj.fake_inr_price);
        changeChecked({...selectedObj});

        MyGA.SendEvent('ln_study_mode', 'ln_study_mode', 'ln_click_study_mode', `${selectedObj.mode}|get_choice_display:"STUDY_MODE"`, '', false, true);
    }

    const goToCart = async (value) => {
        let cartItems = {};
        let addonsId = [];

        if(!product_detail?.redeem_test) {
            MyGA.SendEvent('ln_enroll_now', 'ln_enroll_now', 'ln_click_enroll_now', `${product_detail?.prd_H1}`, '', false, true);
            trackUser({"query" : tracking_data, "action" :'enroll_now'});

            if(frqntProd && frqntProd.length > 0) {
                frqntProd.map(prdId => addonsId.push(prdId.id));
            }

            if(value.id) cartItems = {'prod_id': product_id, 'cart_type': 'cart', 'cv_id': value.id, "addons": addonsId};
            else cartItems = {'prod_id': product_id, 'cart_type': 'cart', 'cv_id': (product_detail?.selected_var ? product_detail?.selected_var?.id : ""), "addons": addonsId};

            try {
                dispatch(startMainCourseCartLoader());
                await new Promise((resolve, reject) => dispatch(fetchAddToCartEnroll({ cartItems ,resolve, reject })));
                dispatch(stopMainCourseCartLoader());
            }
            catch (error) {
                dispatch(stopMainCourseCartLoader());
            }
        }
        else {
            trackUser({"query" : tracking_data, "action" :'redeem_now'});
            cartItems = { 'prod_id': product_detail?.product_id, 'redeem_option': product_detail?.redeem_option }

            try {
                dispatch(startMainCourseCartLoader());
                await new Promise((resolve, reject) => dispatch(fetchAddToCartRedeem({ cartItems ,resolve, reject })));
                dispatch(stopMainCourseCartLoader());
            }
            catch (error) {
                Toast.fire({
                    type: 'error',
                    title: error?.error_message
                });
                dispatch(stopMainCourseCartLoader());
            }
        }
    }

    const getProductPrice = (product) => {
        let price = 0;
        price += frqntProd.reduce((previousValue, currentValue) => {
          return parseFloat(previousValue) + parseFloat(currentValue.inr_price);
        }, 0);
        return parseFloat(product) + price;
    };

    const getDiscountedPrice = (fakeP, realP) => {
        return ((fakeP - realP) / fakeP * 100).toFixed(0);
    }

    const trackJobs = () => {
        trackUser({"query" : tracking_data, "action" :'jobs_available'});
        trackUser({"query" : tracking_data, "action" :'exit_product_page'});
        MyGA.SendEvent('ln_course_details', 'ln_course_details', 'ln_jobs_available', 'Jobs available', '', '', true);
        window.location.href = product_detail?.num_jobs_url;
    }

    const viewAllCourses = () => {
        MyGA.SendEvent('Search',`${product_detail?.prd_vendor}`,'ViewAllProductVendor');
        trackUser({"query" : tracking_data, "action" :'all_courses_or_certifications'});
        trackUser({"query" : tracking_data, "action" :'exit_product_page'});

        window.location.href=`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`;
    }

    const handleBreadCrumbTracking = (data, key, val) => {
        if(data.length - 1 !== key) trackUser({"query" : tracking_data, "action" :'exit_product_page'});
        
        MyGA.SendEvent('ln_breadcrumbs', 'ln_breadcrumbs', 'ln_breadcrumb_click', `${val.name}`, '', false, true);
        window.location.href = `${siteDomain}${val.url}`;
    }

    return (
        <>
            { mainCourseCartLoader ? <Loader /> : ''}

            <header className="container-fluid pos-rel course-detail-bg">
                    <div className="row">
                        <div className="container detail-header-content">
                            <div className="w-65">
                                <Breadcrumb>
                                    {
                                        product_detail?.breadcrumbs?.map((bread, inx) => {
                                            return <Breadcrumb.Item key={inx} onClick={() => handleBreadCrumbTracking(product_detail?.breadcrumbs, inx, bread)}>{bread.name}</Breadcrumb.Item>
                                        })
                                    }
                                </Breadcrumb>
                                <div className="detail-heading" data-aos="fade-right" itemProp="Course" itemScope itemType="https://schema.org/Course">
                                    <div className="detail-heading__icon" itemProp="image">
                                        <figure>
                                            <img src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                                        </figure>
                                    </div>
                                    <div className="detail-heading__content" itemProp="name">
                                        { product_detail?.pTg !== 'None' && <span className="flag-yellowB">{product_detail?.pTg}</span> }
                                        <h1 className="heading1">
                                            {product_detail?.prd_H1}
                                        </h1>
                                        <div className="d-flex mt-15">
                                            {
                                                product_detail?.prd_num_rating ?
                                                <span className="rating">
                                                    {
                                                        product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                                    }
                                                    <span itemProp="ratingValue">{product_detail?.prd_rating?.toFixed()}/5</span>
                                                </span> : ''
                                            }
                                            
                                            {
                                                <>
                                                {product_detail?.prd_num_rating ? <span className="review-jobs cursorLink">
                                                <LinkScroll to={"reviews"}>
                                                    <figure className="icon-reviews-link"></figure> <strong> {product_detail?.prd_num_rating}</strong> Reviews
                                                </LinkScroll>
                                                </span> : ""}
                                                {product_detail?.prd_num_jobs ? <span className="review-jobs">
                                                    <a target="_blank" onClick={() => trackJobs(product_detail?.num_jobs_url)} className="cursorLink">
                                                        <figure className="icon-jobs-link"></figure> <strong>{product_detail?.prd_num_jobs}</strong> Jobs available
                                                    </a>
                                                </span> : ""}
                                                </>
                                            }
                                        </div>
                                    </div>
                                </div>
                                <ul className="course-stats mt-30 mb-20">
                                    <li>
                                        <strong>By <span itemProp="provider" onClick={() => MyGA.SendEvent('ln_course_provider', 'ln_course_provider', 'ln_click_course_provider', `${product_detail?.prd_vendor}` , '', false, true)}>{product_detail?.prd_vendor}</span></strong>
                                        <a onClick={() => viewAllCourses()} className="cursorLink">View all</a> courses by {product_detail?.prd_vendor}  
                                    </li>

                                    {
                                        product_detail?.pop ?
                                        <li>
                                            <LinkScroll className="d-block cursorLink" to={"popListTemplate"} offset={-150}>+{providerCount} more</LinkScroll> Course providers  
                                        </li>
                                        : ""
                                    }

                                    {
                                        product_detail?.duration ?
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-course-duration mr-10"></figure>
                                            <p>
                                                Course Duration <strong>{varChecked?.dur_days || product_detail?.selected_var?.dur_days || '--'} Days</strong>
                                            </p>
                                        </li>
                                        : ""
                                    }
                                    {
                                        product_detail?.access_duration ?
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-access-duration mr-10"></figure>
                                            <p>
                                                Access Duration <strong>{product_detail?.access_duration}</strong>
                                            </p>
                                        </li>
                                        : ""
                                    }

                                    {
                                        product_detail?.prd_asft?.test_duration ?
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-course-duration mr-10"></figure>
                                            <p>
                                                Test Duration <strong>{product_detail?.prd_asft?.test_duration}</strong>
                                            </p>
                                        </li>
                                        : ""
                                    }

                                    {
                                        product_detail?.prd_asft?.number_of_questions ?
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-question-no mr-10"></figure>
                                            <p>
                                                No. of questions <strong>{product_detail?.prd_asft?.number_of_questions}</strong>
                                            </p>
                                        </li>
                                        : ""
                                    }
                                </ul>
                                <ul className="course-stats-btm mt-20 mb-20">
                                    {
                                        (varChecked?.type || product_detail?.selected_var?.type) ? <li>Course Type: <strong>{getStudyMode(varChecked?.type || product_detail?.selected_var?.type)}</strong></li>
                                        : ""
                                    }

                                    {
                                        (varChecked?.level || product_detail?.selected_var?.level) ? <li>Course Level: <strong>{getStudyLevel(varChecked?.level || product_detail?.selected_var?.level)}</strong></li>
                                        : ""
                                    }

                                    {
                                        <li>Certification: <strong>{(varChecked?.certify || product_detail?.selected_var?.certify) === 0 ? 'No' : (varChecked?.certify || product_detail?.selected_var?.certify) === false ? 'No' : 'Yes' }</strong></li>
                                    }
                                </ul>
                                <div className="intro-video">
                                    <figure className="intro-video__img">
                                        <a rel="noopener noreferrer" target="_blank" href={`https://${product_detail?.prd_video}`}>
                                            <iframe src={`https://${product_detail?.prd_video}`} frameBorder="0" />
                                            <i className="icon-play-video"></i>
                                            <strong>Intro video</strong>
                                        </a>
                                    </figure>

                                    <span className="intro-video__content" itemProp="embedUrl">
                                        { completeDescription ? <div id="module" className=" about-course">
                                            {completeDescription?.length > reqLength ? (
                                                <input type="checkbox" onClick={() => setReadAll(!readAll) } className="read-more-state" id="post-10" checked={readAll} itemProp="about" />
                                                ) : (
                                                    ""
                                                    )}
                                                <span className="read-more-wrap" itemProp="description">
                                                    <span dangerouslySetInnerHTML={{__html:completeDescription?.slice(0, readAll ? completeDescription?.length : reqLength)}} />
                                                    {/* <span className="read-more-target" dangerouslySetInnerHTML={{__html: completeDescription?.slice(reqLength)}} /> */}
                                                </span>
                                                <label htmlFor="post-10" className="read-more-trigger"></label>
                                        </div> : "" }
                                    </span>
                                </div>
                            </div>
                            
                            <div className="banner-detail">
                                        <div className="course-enrol">
                                            {  
                                                product_detail?.selected_var && product_detail?.var_list && product_detail?.var_list?.length > 0 &&
                                                <div className="course-enrol__mode">
                                                    Mode
                                                    {
                                                        product_detail?.var_list?.map((varList, indx) => {
                                                            return (
                                                                    <form key={indx}>
                                                                        <label htmlFor={varList?.id}>
                                                                            <input type="radio" name="radio" id={varList?.id} checked={varChecked?.id && (varChecked?.id === varList?.id ? true : false) || !varChecked?.id && (product_detail?.selected_var?.id === varList?.id ? true : false)} onChange={() => changeMode(varList)} />
                                                                            {getStudyMode(varList?.mode)}
                                                                        </label> 
                                                                    </form>
                                                                )
                                                        })
                                                    }
                                                </div>
                                            }
                                            <div className="course-enrol__price">
                                                <strong className="price-taxes mt-20 mb-10">{getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) || product_detail?.pPinb}/-  <span className="taxes">(+taxes)</span></strong>
                                                <strong className="price-offer mt-0 mb-10">
                                                    {
                                                        (varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price) > 0 ?
                                                        <>
                                                            <del>{varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price}/- </del> 
                                                
                                                            <span className="offer">
                                                                {
                                                                    getDiscountedPrice(varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price, varChecked?.inr_price || product_detail?.var_list[0]?.inr_price)
                                                                }
                                                                % Off
                                                            </span>
                                                        </>
                                                        : "" 
                                                    }
                                                    {
                                                        (!product_detail?.var_list?.length > 0 && !product_detail?.selected_var && product_detail?.pPfinb > 0) ?
                                                            <>
                                                                <del>{product_detail?.pPfinb}/- </del>
                                                                <span className="offer">{getDiscountedPrice(product_detail?.pPfinb, product_detail?.pPinb)} % Off</span>
                                                            </>
                                                        : ""
                                                    }
                                                </strong>
                                                <p className="d-flex mb-0">
                                                    <a onClick={() => goToCart(varChecked)} className="btn btn-secondary mt-10 mr-10">{ product_detail?.prd_service === 'assessment' ? 'Buy Now' : product_detail?.redeem_test ? 'Redeem Now' : 'Enroll now' }</a>
                                                    <LinkScroll to={"enquire-now"} className="btn btn-outline-primary mt-10" offset={-220}>Enquire now</LinkScroll>
                                                </p>
                                                
                                            </div>
                                            <div className="course-enrol__offer lightblue-bg2">
                                                {product_detail?.redeem_test && <span>You have {product_detail?.product_redeem_count} free practice test (Assessment) as you're a Shine Premium User</span>}
                                                <strong className="mt-10 mb-5">Offers</strong>
                                                <ul className="pb-0">
                                                {
                                                    (varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) < 5001 ?
                                                    <li><figure className="icon-offer-pay"></figure> <span className="flex-1">Buy now &amp; <strong>pay within 14 days using ePayLater</strong></span> </li>

                                                    :
                                                    
                                                    <li><figure className="icon-offer-pay"></figure> <span className="flex-1">Avail <strong>Interest-free EMIs at no additional cost using Zest Money payment option</strong></span> </li>
                                                }
                                                </ul>
                                            </div>
                                        </div>
                               
                                { product_detail?.combo && <ComboIncludes combo_list={product_detail?.combo_list} /> }
                                { product_detail?.fbt && <FrequentlyBought addFrqntProd={addFrqntProd} frqntProd={frqntProd} fbt_list={product_detail?.fbt_list}/> }
                            </div>
                        </div>
                    </div>
            </header> 
        </>
    )
}

export default BannerCourseDetail;