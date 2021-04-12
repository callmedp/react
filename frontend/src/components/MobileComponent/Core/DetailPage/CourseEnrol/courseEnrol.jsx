import React, { useState } from 'react';
import './courseEnrol.scss';
import {Link} from 'react-router-dom';
import { getStudyMode } from 'utils/detailPageUtils/studyMode';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAddToCartEnroll } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';

const CourseEnrol = (props) => {
    const { product_detail, varChecked, changeChecked } = props;
    const dispatch = useDispatch();
    const { mainCourseCartLoader } = useSelector(store => store.loader);
    const [discountPrice, discountPriceSelected] = useState(0);

    const changeMode = (objj) => {
        let selectedObj = objj;
        discountPriceSelected(objj.fake_inr_price);
        changeChecked({...selectedObj});
    }

    const goToCart = async (value) => {
        let cartItems = {};

        if(value.id) cartItems = {'prod_id': product_detail.pPv, 'cart_type': 'cart', 'cv_id': value.id};
        else cartItems = {'prod_id': product_detail.pPv, 'cart_type': 'cart', 'cv_id': product_detail.selected_var.id};

        try {
            dispatch(startMainCourseCartLoader());
            await new Promise((resolve, reject) => dispatch(fetchAddToCartEnroll({ cartItems ,resolve, reject })));
            dispatch(stopMainCourseCartLoader());
        }
        catch (error) {
            dispatch(stopMainCourseCartLoader());
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
                        <strong className="mt-20 mb-10">{varChecked?.inr_price || product_detail?.var_list[0]?.inr_price}/-&nbsp; 
                            <span>
                                {
                                    varChecked?.id ? 
                                        <del>{discountPrice}</del> 
                                        :
                                        <del>{product_detail?.var_list[0]?.fake_inr_price}</del>
                                }
                                &nbsp;30%off
                            </span>
                        </strong>
                        <Link to={'#'} className="btn btn-secondary mt-10 ml-auto" onClick={() => goToCart(varChecked)}>{ product_detail?.pTF === 16 ? 'Buy Now' : 'Enroll now' }</Link>
                    </div>
                    <div className="m-course-enrol__offer lightblue-bg2">
                        <strong className="mt-10 mb-5">Offers</strong>
                        <ul className="pb-0">
                            {
                                (varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) < 5001 ?
                                <li><figure class="micon-offer-pay"></figure> Buy now &amp; <strong>pay within 14 days using ePayLater</strong> </li>

                                :
                                
                                <li><figure className="micon-offer-pay"></figure> Avail &nbsp; <strong>Interest-free EMIs at no additional cost using Zest Money payment option</strong> </li>
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