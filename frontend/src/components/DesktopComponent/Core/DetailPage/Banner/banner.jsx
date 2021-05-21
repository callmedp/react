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
import { getTrackingInfo, getCandidateId } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { Toast } from '../../../Common/Toast/toast';

const BannerCourseDetail = (props) => {

    const {
        product_detail,
        varChecked,
        changeChecked,
        frqntProd,
        addFrqntProd,
        product_id,
        providerCount,
        completeDescription,
        reqLength,
        showReviewModal,
        pUrl,
        prd_review_list,
        setVideoModal,
        prd_product,
        upc
    } = props;

    const [discountPrice, discountPriceSelected] = useState(0);
    const dispatch = useDispatch();
    const { mainCourseCartLoader } = useSelector(store => store.loader);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+' 
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    const changeMode = (objj) => {
        let selectedObj = objj;
        discountPriceSelected(objj.fake_inr_price);
        changeChecked({...selectedObj});

        MyGA.SendEvent('ln_study_mode', 'ln_study_mode', 'ln_click_study_mode', `${getStudyMode(selectedObj.mode)}`, '', false, true);
    }

    const goToCart = async (value) => {
        let cartItems = {};
        let addonsId = [];
        let tracking_data = getTrackingInfo();

        if(!product_detail?.redeem_test) {
            MyGA.SendEvent('ln_enroll_now', 'ln_enroll_now', 'ln_click_enroll_now', `${product_detail?.prd_H1}`, '', false, true);

            dispatch(trackUser({"query" : tracking_data, "action" :'enroll_now'}));

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
                Toast.fire({
                    type: 'error',
                    title: error?.error_message
                });
                dispatch(stopMainCourseCartLoader());
            }
        }
        else {
            dispatch(trackUser({"query" : tracking_data, "action" :'redeem_now'}));
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
        let tracking_data = getTrackingInfo();

        dispatch(trackUser({"query" : tracking_data, "action" :'jobs_available'}));
        dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));
        MyGA.SendEvent('ln_course_details', 'ln_course_details', 'ln_jobs_available', 'Jobs available', '', '', true);
        window.location.href = product_detail?.num_jobs_url;
    }

    const viewAllCourses = () => {
        let tracking_data = getTrackingInfo();

        MyGA.SendEvent('Search',`${product_detail?.prd_vendor}`,'ViewAllProductVendor');
        dispatch(trackUser({"query" : tracking_data, "action" :'all_courses_or_certifications'}));
        dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));

        window.location.href=`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`;
    }

    const handleBreadCrumbTracking = (data, key, val) => {
        let tracking_data = getTrackingInfo();

        if(data.length - 1 !== key) dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));
        
        MyGA.SendEvent('ln_breadcrumbs', 'ln_breadcrumbs', 'ln_breadcrumb_click', `${val.name}`, '', false, true);
        if(!!val.url) return window.location.href = `${siteDomain}${val.url}`;
    }

    const handleLoginRedirect = () => {
        window.location.href= `${siteDomain}/login/?next=${pUrl}?sm=true`
    }

    const handleVideoModal = (eve) => {
        eve.preventDefault();
        setVideoModal(true);
    }

    const getVideoId = (link) => {
        
        try{
            return new URL(link).searchParams.get('v');
        }catch{
            return ''
        }
    }

    return (
        <>
            { mainCourseCartLoader ? <Loader /> : ''}

            <header className="container-fluid pos-rel course-detail-bg">
                <div className="row">
                    <div className="container detail-header-content">
                        <div className="w-65">
                            <Breadcrumb itemScope itemType="http://schema.org/BreadcrumbList">
                                {
                                    product_detail?.breadcrumbs?.map((bread, inx) => {

                                        return (
                                            bread?.url ? 
                                                <Breadcrumb.Item itemProp="itemListElement" itemScope itemType="http://schema.org/ListItem" key={inx} onClick={() => handleBreadCrumbTracking(product_detail?.breadcrumbs, inx, bread)}>
                                                    <span itemProp="item" content={siteDomain + bread?.url}></span>
                                                    <span itemProp="name">{bread?.name}</span>
                                                    <span itemProp="position" content={inx+1}></span>
                                                </Breadcrumb.Item>
                                            : 
                                                <Breadcrumb.Item key={inx} className="noLinkAnchor">{bread?.name}</Breadcrumb.Item>
                                        )
                                    })
                                }
                            </Breadcrumb>
                            <div className="detail-heading" data-aos="fade-zoom-in">
                                <div className="detail-heading__icon">
                                    <figure>
                                        <img itemProp="image" src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                                    </figure>
                                </div>
                                <div className="detail-heading__content">
                                    { product_detail?.pTg !== 'None' && <span className="flag-yellowB">{product_detail?.pTg}</span> }
                                    <h1 className="heading1" itemProp="name">
                                        {product_detail?.prd_H1}
                                    </h1>
                                    <div className="d-flex mt-15" itemProp="aggregateRating" itemScope itemType="https://schema.org/AggregateRating">
                                        {
                                            product_detail?.prd_num_rating ?
                                            <span className="rating">
                                                {
                                                    product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                                }
                                                <span itemProp="ratingValue" content={product_detail?.prd_rating?.toFixed()}>{product_detail?.prd_rating?.toFixed()}/5</span>
                                            </span> : ''
                                        }
                                        
                                        {
                                            <>
                                                {
                                                    (product_detail?.prd_num_rating > 0 && prd_review_list && prd_review_list?.length) ? 
                                                        <span className="review-jobs cursorLink">
                                                            <LinkScroll to={"reviews"} offset={-160} smooth={true}>
                                                                <figure className="icon-reviews-link"></figure> <strong itemProp="reviewCount" content={product_detail?.prd_num_rating}> {product_detail?.prd_num_rating}</strong> Reviews
                                                            </LinkScroll>
                                                        </span> 
                                                        :
                                                        getCandidateId() ?
                                                            <span className="review-jobs cursorLink" onClick={() => {showReviewModal(true)}} itemProp="reviewCount" content="1">
                                                                <figure className="icon-reviews-link"></figure> Write a Review
                                                            </span> 
                                                            : 
                                                            <span className="review-jobs cursorLink" onClick={() => { handleLoginRedirect() }} itemProp="reviewCount" content="1">
                                                                <figure className="icon-reviews-link"></figure> Write a Review
                                                            </span>    
                                                }

                                                {
                                                    product_detail?.prd_num_jobs ? 
                                                        <span className="review-jobs">
                                                            <a target="_blank" onClick={() => trackJobs(product_detail?.num_jobs_url)} className="cursorLink">
                                                                <figure className="icon-jobs-link"></figure> <strong>{product_detail?.prd_num_jobs}</strong> Jobs available
                                                            </a>
                                                        </span> : ""
                                                }
                                            </>
                                        }
                                    </div>
                                </div>
                            </div>
                            <ul className="course-stats mt-30 mb-20">
                                <li>
                                    <strong itemProp="brand" itemType="http://schema.org/Brand" itemScope>By <span itemProp="name" content={product_detail?.prd_vendor} onClick={() => MyGA.SendEvent('ln_course_provider', 'ln_course_provider', 'ln_click_course_provider', `${product_detail?.prd_vendor}` , '', false, true)}>{product_detail?.prd_vendor}</span></strong>
                                    <a onClick={() => viewAllCourses()} className="cursorLink">View all</a> courses by {product_detail?.prd_vendor}  
                                </li>

                                {
                                    product_detail?.pop ?
                                    <li>
                                        <LinkScroll className="d-block cursorLink" to={"popListTemplate"} offset={-150} smooth={true}>+{providerCount} more</LinkScroll> Course providers  
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
                            <ul className="course-stats-btm mt-20 mb-25">
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
                            {
                                (product_detail?.prd_video || completeDescription) &&
                                    <div className="intro-video">
                                        {
                                            product_detail?.prd_video &&
                                                <figure className="intro-video__img">
                                                    <a rel="noopener noreferrer" onClick={handleVideoModal}>
                                                        <iframe src={`https://www.youtube.com/embed/${getVideoId(product_detail?.prd_video)}`} frameBorder="0" />
                                                        <i className="icon-play-video"></i>
                                                        <strong>Intro video</strong>
                                                    </a>
                                                </figure>    
                                        }

                                        
                                        { completeDescription && 
                                            <span className="intro-video__content">
                                                <div id="module" className="about-course">
                                                        <span className="read-more-wrap">
                                                            <span itemProp="description" content={completeDescription} dangerouslySetInnerHTML={{__html:completeDescription?.slice(0, reqLength) + ((completeDescription?.length > reqLength) ? '....' : '')}} />
                                                        </span>
                                                        {
                                                            completeDescription?.length > reqLength ? 
                                                            (
                                                                <LinkScroll to = {'aboutsection'} offset={-160} smooth={true}> Read More</LinkScroll> 
                                                            )
                                                            : ("")
                                                        }
                                                </div> 
                                            </span>
                                        }
                                    </div>
                            }
                        </div>
                        
                        <div className="banner-detail">
                            <div className="course-enrol" itemProp="offers" itemScope itemType="http://schema.org/Offer">
                                {  
                                    product_detail?.selected_var && product_detail?.var_list && product_detail?.var_list?.length > 0 &&
                                    <div className="course-enrol__mode">
                                        Mode
                                        {
                                            product_detail?.var_list?.map((varList, indx) => {
                                                return (
                                                        <form key={indx}>
                                                            <label htmlFor={varList?.id} itemProp={varList?.mode === 'OL' ? `availability` : ''} content={varList?.mode === 'OL' ? "https://schema.org/OnlineOnly" : ''}>
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
                                    <strong className="price-taxes mt-20 mb-10">
                                        {getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb)}/- <span className="taxes">(+taxes)</span>
                                    </strong>
                                    
                                    {/* meta tags for price */}
                                    <span itemProp="price" content={getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb)}></span>
                                    <span itemProp="priceCurrency" content="INR"></span>
                                    <span itemProp="priceValidUntil" content={new Date()}></span>
                                    <span itemProp="url" content={siteDomain+product_detail?.canonical_url}></span>

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
                                        <LinkScroll to={"enquire-now"} className="btn btn-outline-primary mt-10" offset={-160} smooth={true}>Enquire now</LinkScroll>
                                    </p>
                                    
                                </div>
                                <div className="course-enrol__offer lightblue-bg2">
                                    {product_detail?.redeem_test && <span className="flex-1">You have {product_detail?.product_redeem_count} free practice test (Assessment) as you're a Shine Premium User</span>}
                                    <strong className="mt-10 mb-5">Offers</strong>
                                    <ul className="pb-0">
                                    {
                                        (varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) < 5001 ?
                                        <li><figure className="icon-offer-pay"></figure> <span className="flex-1">Buy now &amp; <strong>pay within 14 days using ePayLater</strong></span> </li>

                                        :
                                        
                                        <li><figure className="icon-offer-pay"></figure> <span className="flex-1">Avail <strong>Interest-free EMIs at no additional cost using Zest Money payment option</strong></span> </li>
                                    }
                                    {
                                        product_detail?.free_test && <li><figure className="icon-offer-test"></figure><span className="flex-1">Take <strong>free practice test</strong> to enhance your skill</span></li>
                                    }
                                    </ul>
                                </div>
                            </div>
                    
                            { product_detail?.combo && <ComboIncludes combo_list={product_detail?.combo_list} /> }
                            { product_detail?.fbt && <FrequentlyBought addFrqntProd={addFrqntProd} frqntProd={frqntProd} fbt_list={product_detail?.fbt_list}/> }
                        </div>
                    </div>
                </div>

                {/* meta tags common */}
                <span itemProp="sku" content={prd_product}></span>
                <span itemProp="mpn" content={upc}></span>
            </header> 
        </>
    )
}

export default BannerCourseDetail;