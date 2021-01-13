import React, { useState } from 'react';
import Slider from "react-slick";
import { siteDomain } from 'utils/domains';

const ProductCards = props => {
    const {
        productList
    } = props

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

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> : 
            star === '+' ? <em className="micon-halfstar" key={index}></em> : 
                           <em className="micon-blankstar" key={index}></em>
        )
    }

    return (
        <Slider {...settings}>
            {
                productList?.map((product, index) => {
                    return (
                        <div className="m-card" key={index}>
                            <div className="m-card__heading">
                                <figure>
                                    <img src={product?.imgUrl} alt={product?.imgAlt} />
                                </figure>
                                <h3 className="m-heading3">
                                    <a href={`${siteDomain}${product.url}`}>{product?.name}</a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="mr-10">By { product?.providerName?.length > 17 ? product?.providerName?.slice(0, 17) + '...' : product?.providerName }</span>
                                <span className="m-rating">
                                    { product?.stars?.map((star, index) => starRatings(star, index)) }
                                    <span>{product?.rating?.toFixed(1)}/5</span>
                                </span>
                                </div>
                                <div className="m-card__price">
                                    <strong>{product?.price}/-</strong> 
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