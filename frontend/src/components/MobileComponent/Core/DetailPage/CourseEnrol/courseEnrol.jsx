import React, { useState } from 'react';
import './courseEnrol.scss';
import {Link} from 'react-router-dom';
import { getStudyMode } from 'utils/detailPageUtils/studyMode';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAddToCartEnroll, fetchAddToCartRedeem } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';
import { showSwal } from 'utils/swal';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const CourseEnrol = (props) => {
    const { product_detail, varChecked, changeChecked, getProductPrice, frqntProd, product_id } = props;
    const dispatch = useDispatch();
    const { mainCourseCartLoader } = useSelector(store => store.loader);
    const [discountPrice, discountPriceSelected] = useState(0);
    const tracking_data = getTrackingInfo();

    const changeMode = (objj) => {
        let selectedObj = objj;
        discountPriceSelected(objj.fake_inr_price);
        changeChecked({...selectedObj});
        MyGA.SendEvent('ln_study_mode', 'ln_study_mode', 'ln_click_study_mode', `${selectedObj.mode}|get_choice_display:"STUDY_MODE"`, '', false, true);
    }

    const getDiscountedPrice = (fakeP, realP) => {
        return ((fakeP - realP) / fakeP * 100).toFixed(0);
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
                showSwal('error', error?.error_message);
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
                showSwal('error', error?.error_message);
                dispatch(stopMainCourseCartLoader());
            }
        }
    }

    return (
        <>
            { mainCourseCartLoader ? <Loader /> : ''}

            <section className="m-container mt-80n mb-0 pb-0">
                <div className="m-course-enrol">
                    {
                        product_detail?.var_list?.length > 0 && 
                            <div className="m-course-enrol__mode"> 
                                <form>
                                    <strong>Mode</strong>
                                    {
                                        product_detail?.var_list?.map((varList) => {
                                            return (
                                                <label key={varList.id}>
                                                    <input type="radio" name="radio" id={varList.id} checked={varChecked?.id && (varChecked?.id === varList.id ? true : false) || !varChecked?.id && (product_detail?.selected_var?.id === varList.id ? true : false)} onChange={() => changeMode(varList)} />
                                                    {getStudyMode(varList?.mode)}
                                                </label>
                                            )
                                        })
                                    }
                                </form>
                            </div>
                    }

                    <div className="m-course-enrol__price">
                        <strong className="mt-20 mb-10">{getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb)}/-&nbsp; 
                            {
                                (varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price) > 0 ?
                                <span>
                                    {
                                        varChecked?.id ? 
                                            <del>{discountPrice}</del> 
                                            :
                                            <del>{product_detail?.var_list[0]?.fake_inr_price}</del>
                                    }
                                    &nbsp;
                                    {
                                        getDiscountedPrice(varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price, varChecked?.inr_price || product_detail?.var_list[0]?.inr_price)
                                    }%off
                                </span>
                                : ""
                            }

                            {
                                (!product_detail?.var_list?.length > 0 && !product_detail?.selected_var && product_detail?.pPfinb > 0) ?
                                <span>
                                    <del>{product_detail?.pPfinb}</del> 
                                    &nbsp;
                                    {
                                        getDiscountedPrice(product_detail?.pPfinb, product_detail?.pPinb)
                                    }%off
                                </span>
                                : ""
                            }

                        </strong>
                        <Link to={'#'} className="btn btn-secondary mt-10 ml-auto" onClick={() => goToCart(varChecked)}> { product_detail?.prd_service === 'assessment' ? 'Buy Now' : product_detail?.redeem_test ? 'Redeem Now' : 'Enroll now' }</Link>
                    </div>
                    <div className="m-course-enrol__offer lightblue-bg2">
                        {product_detail?.redeem_test && <span>You have {product_detail?.product_redeem_count} free practice test (Assessment) as you're a Shine Premium User</span>}
                        <strong className="mt-10 mb-5">Offers</strong>
                        <ul className="pb-0">
                            {
                                (varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) < 5001 ?
                                <li><figure className="micon-offer-pay"></figure> <span className="flex-1">Buy now <strong>pay within 14 days using ePayLater</strong></span> </li>

                                :
                                
                                <li><figure className="micon-offer-pay"></figure> <span className="flex-1">Avail <strong>Interest-free EMIs at no additional cost using Zest Money payment option</strong></span> </li>
                            }
                            {
                                product_detail?.free_test && <li><figure className="micon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                            }
                            {/* <li><figure className="micon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                            <li><figure className="micon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                            <li><figure className="micon-offer-global"></figure> <strong>Global</strong> Education providers</li> */}
                        </ul>
                        {/* <Link to={"#"}>+2 more</Link> */}
                    </div>
                </div>
            </section>
        </>
    )
}

export default CourseEnrol;