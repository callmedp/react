import React, {useState} from 'react';
// import {Link} from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNavDetail.scss';
import { Link as LinkScroll } from "react-scroll";
import { useSelector, useDispatch } from 'react-redux';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { fetchAddToCartEnroll } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';

const StickyNav = (props) => {
    const { product_detail, varChecked, outline, faq, frqntProd } = props;
    const dispatch = useDispatch();
    const [tab, setTab] = useState('1');
    const { mainCourseCartLoader } = useSelector(store => store.loader);

    const handleTab = (event) => {
        setTab(event.target.id)
    }

    const goToCart = async (value) => {
        let cartItems = {};

        if(value.id) cartItems = {'prod_id': product_detail?.pPv, 'cart_type': 'cart', 'cv_id': value.id};
        else cartItems = {'prod_id': product_detail?.pPv, 'cart_type': 'cart', 'cv_id': product_detail?.selected_var.id};

        try {
            dispatch(startMainCourseCartLoader());
            await new Promise((resolve, reject) => dispatch(fetchAddToCartEnroll({ cartItems ,resolve, reject })));
            dispatch(stopMainCourseCartLoader());
        }
        catch (error) {
            dispatch(stopMainCourseCartLoader());
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
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <h2>Digital Marketing Courses & Certification</h2>
                        </span>
                        <Nav>
                            <LinkScroll offset={-160} className={ tab === '1' ? "active" : '' } to={"keyfeatures"} id='1' onClick={handleTab}>Key Features</LinkScroll>
                            
                            {
                                outline && <LinkScroll to={"courseoutline"} offset={-140} className={ tab === '2' ? "active" : '' } id='2' onClick={handleTab}>Outline</LinkScroll>
                            }
                            
                            {/* <LinkScroll offset={-120} to={"outcome"} className={ tab === '3' ? "active" : '' } id='3' onClick={handleTab}>Outcome</LinkScroll> */}
                            
                            <LinkScroll offset={-130} to={"howitworks"} className={ tab === '4' ? "active" : '' } id='4' onClick={handleTab}>How it works</LinkScroll>

                            {
                                faq && <LinkScroll to="faqs" offset={-180} className={ tab === '5' ? "active" : '' } id='5' onClick={handleTab}>FAQs</LinkScroll>
                            }

                            <LinkScroll to={"reviews"} offset={-200} className={ tab === '6' ? "active" : '' } id='6' onClick={handleTab}>Reviews</LinkScroll>
                        </Nav>
                    </div>
                    <Form inline className="course-enrol-sticky">
                        <strong className="mt-20">{getProductPrice(varChecked?.inr_price || product_detail?.var_list[0]?.inr_price)}
                        <del>{varChecked?.id ? varChecked.fake_inr_price : product_detail?.selected_var?.fake_inr_price}</del>
                        </strong>
                        <span className="d-flex">
                            <LinkScroll offset={-220} to={"enquire-now"} className="btn btn-outline-primary">Enquire now</LinkScroll>
                            <a onClick={() => goToCart(varChecked)} className="btn btn-secondary ml-10">Enroll now</a>
                        </span>
                    </Form>
                </div> 
            </Navbar>
        </>
    )
}

export default StickyNav;