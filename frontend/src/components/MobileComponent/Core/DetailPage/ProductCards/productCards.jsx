import React, { useState } from 'react';
import Slider from "react-slick";
import { siteDomain } from 'utils/domains';
import '../../../Common/ProductCardsSlider/productCardsSlider';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { useDispatch } from 'react-redux';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const ProductCards = props => {
    const {
        productList, page_section
    } = props;
    const sendLearningTracking = useLearningTracking();

    const settings = {
        dots: false,
        arrows: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };

    const dispatch = useDispatch();

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const handleTracking = (heading, vendor, idx) => {
        let tracking_data = getTrackingInfo();

        dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));
        dispatch(trackUser({"query" : tracking_data, "action" :'recommended_products'}));

        sendLearningTracking({
            productId: '',
            event: `course_detail_${page_section}_${stringReplace(heading)}_vendor_${stringReplace(vendor)}_${idx}_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: `${page_section}`,
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: idx,
        })
    }

    return (
        <Slider {...settings}>
            {
                productList?.map((product, index) => {
                    return (
                        <div className="m-card" key={index}>
                            <div className="m-card__heading">
                                <figure>
                                    { (product?.pImg || product?.vendor_image) && <img src={product?.pImg || product?.vendor_image } alt={product?.name || product?.pNm || product?.heading || product?.display_name} /> }
                                </figure>
                                <h3 className="m-heading3">
                                    <a onClick={() => handleTracking(product?.name || product?.pNm || product?.heading, product?.vendor, index)} href={`${siteDomain}${product.pURL || product?.url}`}>{(product?.name || product?.pNm || product?.heading || product?.display_name)?.length > 42 ? (product?.name || product?.pNm || product?.heading || product?.display_name)?.slice(0, 42) + '...' : (product?.name || product?.pNm || product?.heading || product?.display_name) }</a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                    <span className="mr-10">
                                        By { (product.pPvn || product.pViA || product?.vendor)?.split(' ')[0]?.length > 13 ? (product.pPvn || product.pViA || product?.vendor)?.split(' ')[0]?.slice(0, 13) + '...' : (product.pPvn || product.pViA || product?.vendor)?.split(' ')[0] }
                                    </span>

                                    <span className="m-rating">
                                        { (product?.pStar || product?.rating)?.map((star, index) => starRatings(star, index)) }
                                        { (product?.pARx || product?.avg_rating) ? <span>{product?.pARx || parseFloat(product?.avg_rating)?.toFixed(1)}/5</span> : ''}
                                    </span>
                                </div>
                                <div className="m-card__price">
                                    <strong>{product?.pPin || product?.inr_price || parseInt(product?.price)}/-</strong>
                                </div>
                            </div>
                        </div>
                    )
                })
            }
        </Slider>
    )
}

export default ProductCards;