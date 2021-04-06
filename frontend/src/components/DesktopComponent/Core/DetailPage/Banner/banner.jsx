import React, { useRef, useEffect, useState } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import { Link as LinkScroll } from 'react-scroll';
import { startMainCourseCartLoader, stopMainCourseCartLoader } from 'store/Loader/actions/index';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAddToCartEnroll } from 'store/DetailPage/actions';
import Loader from '../../../Common/Loader/loader';
import { siteDomain } from 'utils/domains';
import { getStudyMode } from 'utils/detailPageUtils/studyMode';

const BannerCourseDetail = (props) => {
    const {product_detail, varChecked, changeChecked} = props;
    const reqLength = 365;
    const inputCheckbox = useRef(null);
    const regex = /<(.|\n)*?>/g;
    const [discountPrice, discountPriceSelected] = useState(0);
    const dispatch = useDispatch();
    const { mainCourseCartLoader } = useSelector(store => store.loader);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+' 
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    useEffect(() => {
        inputCheckbox.current && (inputCheckbox.current.checked = false);
    })

    const changeMode = (objj) => {
        let selectedObj = objj;
        discountPriceSelected(objj.fake_inr_price);
        changeChecked({...selectedObj});
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

    return (
        <>
            { mainCourseCartLoader ? <Loader /> : ''}

            <header className="container-fluid pos-rel course-detail-bg">
                    <div className="row">
                        <div className="container detail-header-content">
                            <div className="flex-1">
                                <Breadcrumb>
                                    {
                                        product_detail?.breadcrumbs?.map((bread, inx) => {
                                            return <Breadcrumb.Item key={inx} href={bread.url}>{bread.name}</Breadcrumb.Item>
                                        })
                                    }
                                </Breadcrumb>
                                <div className="detail-heading" data-aos="fade-right">
                                    <div className="detail-heading__icon">
                                        <figure>
                                            <img src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                                        </figure>
                                    </div>
                                    <div className="detail-heading__content">
                                        { product_detail?.pTg && <span className="flag-yellowB">{product_detail?.pTg}</span> }
                                        <h1 className="heading1">
                                            {product_detail?.prd_H1}
                                        </h1>
                                        <div className="d-flex mt-15">
                                            <span className="rating">
                                                {
                                                    product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                                }
                                                <span>{product_detail?.prd_rating?.toFixed()}/5</span>
                                            </span>
                                            {
                                                <>
                                                {product_detail?.prd_num_rating ? <span className="review-jobs">
                                                <LinkScroll to={"reviews"}>
                                                    <figure className="icon-reviews-link"></figure> <strong> {product_detail?.prd_num_rating}</strong> Reviews
                                                </LinkScroll>
                                                </span> : ""}
                                                {product_detail?.prd_num_jobs ? <span className="review-jobs">
                                                    <a target="_blank" href={product_detail?.num_jobs_url}>
                                                        <figure className="icon-jobs-link"></figure> <strong>{product_detail?.prd_num_jobs}</strong> Jobs available
                                                    </a>
                                                </span> : ""}
                                                </>
                                            }
                                        </div>
                                    </div>
                                </div>
                                <ul className="course-stats mt-30 mb-30">
                                    <li>
                                        <strong>By {product_detail?.prd_vendor}</strong> <a onClick={() => window.location.href=`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`}>View all</a> courses by {product_detail?.prd_vendor}  
                                    </li>

                                    {
                                        product_detail?.pop &&
                                        <li>
                                            <LinkScroll className="d-block" to={"popListTemplate"}>+4 more</LinkScroll> Course providers  
                                        </li> 
                                    }

                                    {
                                        product_detail?.duration ?
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-course-duration mr-10"></figure>
                                            <p>
                                                Course Duration <strong>{varChecked?.dur_days || product_detail?.selected_var.dur_days} Days</strong>
                                            </p>
                                        </li>
                                    : ""}
                                    {
                                        product_detail?.access_duration &&
                                        <li className="d-flex align-items-center">
                                            <figure className="icon-access-duration mr-10"></figure>
                                            <p>
                                                Access Duration <strong>{product_detail?.access_duration}</strong>
                                            </p>
                                        </li>
                                    }
                                </ul>
                                <div className="intro-video">
                                    <figure className="intro-video__img">
                                        <a rel="noopener noreferrer" target="_blank" href={`https://${product_detail?.prd_video}`}>
                                            <img src={product_detail?.prd_vendor_img} alt="Intro Video" />
                                            {/* <i className="icon-play-video"></i> */}
                                            <strong>Intro video</strong>
                                        </a>
                                    </figure>

                                    <span className="intro-video__content">
                                        { product_detail?.prd_about ? <div id="module" className="row about-course">
                                            {product_detail?.prd_about.replace(regex, '')?.length > reqLength ? (
                                                <input type="checkbox" className="read-more-state" id="post-10" ref={inputCheckbox} itemProp="about" />
                                                ) : (
                                                    ""
                                                    )}
                                                    
                                            <span className="read-more-wrap">
                                                <span dangerouslySetInnerHTML={{__html:product_detail?.prd_about?.replace(regex, '').slice(0, reqLength)}} />
                                                <span className="read-more-target" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(regex, '').slice(reqLength)}} />
                                            </span>
                                            <label htmlFor="post-10" className="read-more-trigger"></label>
                                        </div> : "" }
                                    </span>
                                </div>
                            </div>
                            {
                                product_detail?.selected_var && product_detail?.var_list && product_detail?.var_list?.length > 0 &&
                                <div className="banner-detail">
                                    <div className="course-enrol">
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
                                            {varChecked?.id }{ product_detail?.selected_var?.id}
                                        <div className="course-enrol__price">
                                            <strong className="mt-20 mb-10">{varChecked?.inr_price || product_detail?.var_list[0]?.inr_price}/- 
                                            <del>{varChecked?.id ? discountPrice : product_detail?.var_list[0]?.fake_inr_price}/-</del></strong>
                                            <a onClick={() => goToCart(varChecked)} className="btn btn-secondary mt-10">Enroll now</a>
                                            <LinkScroll to={"enquire-now"} className="btn btn-outline-primary mt-10">Enquire now</LinkScroll>
                                        </div>
                                        <div className="course-enrol__offer lightblue-bg2">
                                            <strong className="mt-10 mb-5">Offers</strong>
                                            <ul className="pb-0">
                                            {
                                                (varChecked?.inr_price || product_detail?.var_list[0]?.inr_price) < 5001 ?
                                                <li><figure className="icon-offer-pay"></figure> Buy now & &nbsp;<strong>make payment within 14 days using ePayLater</strong> </li>

                                                :
                                                
                                                <li><figure className="icon-offer-pay"></figure> Avail &nbsp; <strong>Interest-free EMIs at no additional cost using Zest Money payment option</strong> </li>
                                            }
                                                {/* <li><figure className="icon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                                                <li><figure className="icon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                                                <li><figure className="icon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                                                <li><figure className="icon-offer-global"></figure> <strong>Global</strong> Education providers</li> */}
                                            </ul>
                                            {/* <LinkScroll to={"#"}>+2 more</LinkScroll> */}
                                        </div>
                                    </div>
                                </div>
                            }
                        </div>
                    </div>
            </header> 
        </>
    )
}

export default BannerCourseDetail;