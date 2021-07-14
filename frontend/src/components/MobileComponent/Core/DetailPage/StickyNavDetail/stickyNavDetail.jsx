import React, { useState } from 'react';
import './stickyNavDetail.scss';
import {Link} from 'react-router-dom';
import Slider from "react-slick";
import { Link as LinkScroll } from "react-scroll";
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useDispatch } from 'react-redux';
import { fetchAddToCartEnroll, fetchAddToCartRedeem } from 'store/DetailPage/actions';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { showSwal } from 'utils/swal';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const StickyNavDetail = (props) => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    }

    const { product_detail, varChecked, outline, faq, frqntProd, topics, product_id, prd_review_list, hasKeyFeatures, hasWhatYouGet } = props;
    const sendLearningTracking = useLearningTracking();
    const [tab, setTab] = useState('1');
    const dispatch = useDispatch();
    let category_name = stringReplace(product_detail?.breadcrumbs[1].name) || stringReplace(product_detail?.breadcrumbs[2].name);

    const handleTab = (event) => {
        setTab(event.target.id)
    }

    const getProductPrice = (product) => {
        let price = 0;
        price += frqntProd.reduce((previousValue, currentValue) => {
          return parseFloat(previousValue) + parseFloat(currentValue.inr_price);
        }, 0);
        return parseFloat(product) + price;
    };

    const addToCartTracking = (title) => {
        sendLearningTracking({
            productId: '',
            event: title,
            pageTitle:'course_detail',
            sectionPlacement: 'sticky_nav',
            eventCategory: stringReplace(product_detail?.prd_H1),
            eventLabel: category_name,
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const goToCart = async (value) => {
        let cartItems = {};
        let addonsId = [];
        let tracking_data = getTrackingInfo();

        if(!product_detail?.redeem_test) {
            MyGA.SendEvent('ln_enroll_now', 'ln_enroll_now', 'ln_click_enroll_now', `${product_detail?.prd_H1}`, '', false, true);
            dispatch(trackUser({"query" : tracking_data, "action" :'enroll_now'}));
            addToCartTracking(`course_detail_sticky_nav_${stringReplace(product_detail?.prd_H1)}_${product_id}_enroll_now_clicked`);

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
                showSwal('error', error?.error_message);
                dispatch(stopMainCourseCartLoader());
            }
        }
        else {
            dispatch(trackUser({"query" : tracking_data, "action" :'redeem_now'}));
            addToCartTracking(`course_detail_sticky_nav_${stringReplace(product_detail?.prd_H1)}_${product_id}_redeem_now_clicked`);
            cartItems = { 'prod_id': product_detail?.product_id, 'redeem_option': product_detail?.redeem_option }

            try {
                dispatch(startMainCourseCartLoader());
                await new Promise((resolve, reject) => dispatch(fetchAddToCartRedeem({ cartItems ,resolve, reject })));
                dispatch(stopMainCourseCartLoader());
            }
            catch (error) {
                showSwal('error', error?.error_message);
                dispatch(stopMainCourseCartLoader());
            }
        }
    }

    const trackScrollMenu = (name, ev) => {
        handleTab(ev);
        sendLearningTracking({
            productId: '',
            event: `course_detail_sticky_nav_${stringReplace(product_detail?.prd_H1)}_${product_id}_${name}_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'sticky_nav',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
            <div className="m-sticky-detail m-container mt-0 mb-0 p-0" data-aos="fade-down">
                <div className="m-sticky-detail__price">
                    <strong className="mt-10 mb-10">{getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb)}/-&nbsp; 
                        {
                            (varChecked?.id ? varChecked.fake_inr_price > 0 : product_detail?.selected_var?.fake_inr_price > 0) ? 
                            <del>{varChecked?.id ? varChecked.fake_inr_price : product_detail?.selected_var?.fake_inr_price}</del> 
                            : 
                            (!varChecked?.id && !product_detail?.selected_var && product_detail?.pPfinb > 0) ? <del>{product_detail?.pPfinb}</del> : ''
                        }
                    </strong>
                    <Link to={'#'} className="btn btn-secondary ml-auto" onClick={() => goToCart(varChecked)}>{ product_detail?.prd_service === 'assessment' ? 'Buy Now' : product_detail?.redeem_test ? 'Redeem Now' : 'Buy now' }</Link>
                </div>
                <div className="m-sticky-detail__nav">
                    <Slider {...settings}>
                        {
                            hasKeyFeatures &&
                                <LinkScroll to="features" offset={-120}>
                                    <Link className={ tab === '1' ? "active" : '' } to={"#"} id='1' onClick={ (event) => trackScrollMenu('key_features', event) }>Key Features</Link>
                                </LinkScroll>
                        }

                        {
                            hasWhatYouGet && 
                                <LinkScroll to="whatyouget" offset={-120}>
                                    <Link className={ tab === '10' ? "active" : '' } to={"#"} id='10' onClick={ (event) => trackScrollMenu('key_features', event) }>What You Get</Link>
                                </LinkScroll>
                        }

                        {
                            outline && 
                                <LinkScroll to="m-faq" offset={-120}>
                                    <Link to={"#"} className={ tab === '2' ? "active" : '' } id='2' onClick={ (event) => trackScrollMenu('key_features', event) }>Outline</Link>
                                </LinkScroll>
                        }
                        
                        {/* <LinkScroll to="outcome" offset={-120}>
                            <Link to={"#"} className={ tab === '3' ? "active" : '' } id='3' onClick={ (event) => trackScrollMenu('key_features', event) }>Outcome</Link>
                        </LinkScroll> */}
                        <LinkScroll to="begin" offset={-120}>
                            <Link to={"#"} className={ tab === '4' ? "active" : '' } id='4' onClick={ (event) => trackScrollMenu('key_features', event) }>How it works</Link>
                        </LinkScroll>

                        {
                            topics && 
                                <LinkScroll to="topicsCovered" offset={-170}>
                                    <Link to={"#"} className={ tab === '5' ? "active" : '' } id='5' onClick={ (event) => trackScrollMenu('key_features', event) }>Topics Covered</Link>
                                </LinkScroll>
                        }

                        {
                            faq &&
                                <LinkScroll to="faq" offset={-120}>
                                    <Link to={"#"} className={ tab === '6' ? "active" : '' } id='6' onClick={ (event) => trackScrollMenu('key_features', event) }>FAQ</Link>
                                </LinkScroll>
                        }
                        {
                            (product_detail?.prd_num_rating > 0 && prd_review_list && prd_review_list?.length > 0) &&
                                <LinkScroll to="reviews" offset={-120}>
                                    <Link to={"#"} className={ tab === '7' ? "active" : '' } id='7' onClick={ (event) => trackScrollMenu('key_features', event) }>Reviews</Link>
                                </LinkScroll>
                        }
                    </Slider>
                </div>
            </div>
    )
}

export default StickyNavDetail;