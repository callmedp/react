import React, {useState} from 'react';
// import {Link} from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNavDetail.scss';
import { Link as LinkScroll } from "react-scroll";
import { useSelector, useDispatch } from 'react-redux';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { fetchAddToCartEnroll, fetchAddToCartRedeem } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { Toast } from '../../../Common/Toast/toast';

const StickyNav = (props) => {
    const { product_detail, varChecked, outline, faq, frqntProd, topics, product_id, hasReview } = props;
    const dispatch = useDispatch();
    // const [tab, setTab] = useState('1');
    const { mainCourseCartLoader } = useSelector(store => store.loader);
    const tracking_data = getTrackingInfo();

    const goToCart = async (value) => {
        let cartItems = {};
        let addonsId = [];

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

    return(
        <>
            { mainCourseCartLoader ? <Loader /> : ''}

            <Navbar className="container-fluid lightblue-bg sticky-nav-detail" expand="lg" data-aos="fade-down">
                <div className="container">
                    <div className="flex-1">
                        <span className="d-flex">
                            <figure className="sticky-icon-thumb">
                                <img src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                            </figure>
                            <h2>{product_detail?.prd_H1}</h2>
                        </span>
                        <Nav>
                            <LinkScroll offset={-160} isDynamic={true} spy={true} to="keyfeatures" id='1' smooth={true}>
                                <Nav.Link>
                                    Key Features
                                </Nav.Link>
                            </LinkScroll>
                            
                            {
                                outline && 
                                    <LinkScroll to="courseoutline" offset={-140} isDynamic={true} spy={true} id='2' smooth={true}>
                                        <Nav.Link>
                                            Outline
                                        </Nav.Link>
                                    </LinkScroll>
                            }
                            
                            {/* <LinkScroll offset={-120} to={"outcome"} className={ tab === '3' ? "active" : '' } id='3' onClick={handleTab}>Outcome</LinkScroll> */}
                            
                            <LinkScroll offset={-130} to="howitworks" isDynamic={true} spy={true} id='4' smooth={true}>
                                <Nav.Link>
                                    How it works
                                </Nav.Link>
                            </LinkScroll>

                            {
                                topics && 
                                    <LinkScroll to="topicsCovered" offset={-170} isDynamic={true} spy={true} id='2' smooth={true}>
                                        <Nav.Link>
                                            Topics Covered
                                        </Nav.Link>
                                    </LinkScroll>
                            }

                            {
                                faq && <LinkScroll to="faqs" offset={-200} isDynamic={true} spy={true} id='5' smooth={true}>
                                    <Nav.Link>
                                        FAQs
                                    </Nav.Link>
                                </LinkScroll>
                            }

                            {
                                hasReview &&  
                                    <LinkScroll to="reviews" offset={-160} isDynamic={true} spy={true} id='6' smooth={true}>
                                        <Nav.Link>
                                            Reviews
                                        </Nav.Link>
                                    </LinkScroll>
                            }
                        </Nav>
                    </div>
                    <Form inline className="course-enrol-sticky">
                        { 
                            (varChecked?.inr_price || product_detail?.var_list?.length > 0 || product_detail?.pPinb ) ? 
                            <strong className="mt-20">{getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price || product_detail?.pPinb)}
                                {
                                    (varChecked?.id ? varChecked.fake_inr_price > 0 : product_detail?.selected_var?.fake_inr_price > 0) ? 
                                    <del>{varChecked?.id ? varChecked.fake_inr_price : product_detail?.selected_var?.fake_inr_price}</del> 
                                    : 
                                    (!varChecked?.id && !product_detail?.selected_var && product_detail?.pPfinb > 0) ? <del>{product_detail?.pPfinb}</del> : ''
                                }
                            </strong>
                            : ""
                        }
                        <span className="d-flex">
                            <LinkScroll offset={-160} to={"enquire-now"} className="btn btn-outline-primary" smooth={true}>Enquire now</LinkScroll>
                            <a onClick={() => goToCart(varChecked)} className="btn btn-secondary ml-10">{ product_detail?.prd_service === 'assessment' ? 'Buy Now' : product_detail?.redeem_test ? 'Redeem Now' : 'Enroll now' }</a>
                        </span>
                    </Form>
                </div> 
            </Navbar>
        </>
    )
}

export default StickyNav;