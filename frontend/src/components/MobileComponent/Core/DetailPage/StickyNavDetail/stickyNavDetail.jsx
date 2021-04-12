import React, { useState } from 'react';
import './stickyNavDetail.scss';
import {Link} from 'react-router-dom';
import Slider from "react-slick";
import { Link as LinkScroll } from "react-scroll";
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAddToCartEnroll } from 'store/DetailPage/actions';
// import 'slick-carousel/slick/slick.css';

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

    const { product_detail, varChecked, outline, faq, frqntProd } = props;
    const [tab, setTab] = useState('1')
    const dispatch = useDispatch()

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
                    <Link to={'#'} className="btn btn-secondary ml-auto" onClick={() => goToCart(varChecked)}>{ product_detail?.pTF === 16 ? 'Buy Now' : 'Enroll now' }</Link>
                </div>
                <div className="m-sticky-detail__nav">
                    <Slider {...settings}>
                        <LinkScroll to="features" offset={-120}>
                            <Link className={ tab === '1' ? "active" : '' } to={"#"} id='1' onClick={handleTab}>Key Features</Link>
                        </LinkScroll>
                        {
                            outline && 
                                <LinkScroll to="m-faq" offset={-120}>
                                    <Link to={"#"} className={ tab === '2' ? "active" : '' } id='2' onClick={handleTab}>Outline</Link>
                                </LinkScroll>
                        }
                        
                        {/* <LinkScroll to="outcome" offset={-120}>
                            <Link to={"#"} className={ tab === '3' ? "active" : '' } id='3' onClick={handleTab}>Outcome</Link>
                        </LinkScroll> */}
                        <LinkScroll to="begin" offset={-120}>
                            <Link to={"#"} className={ tab === '4' ? "active" : '' } id='4' onClick={handleTab}>How it works</Link>
                        </LinkScroll>
                        {
                            faq &&
                                <LinkScroll to="faq" offset={-120}>
                                    <Link to={"#"} className={ tab === '5' ? "active" : '' } id='5' onClick={handleTab}>FAQ</Link>
                                </LinkScroll>
                        }
                        {
                            product_detail?.prd_num_rating > 0 &&
                                <LinkScroll to="reviews" offset={-120}>
                                    <Link to={"#"} className={ tab === '6' ? "active" : '' } id='6' onClick={handleTab}>Reviews</Link>
                                </LinkScroll>
                        }
                    </Slider>
                </div>
            </div>
    )
}

export default StickyNavDetail;