// React-Core Import
import React, { useState } from 'react';
import Slider from "react-slick";
import { siteDomain } from 'utils/domains';
import { useSelector, useDispatch } from 'react-redux';

// API Import 
import { fetchInDemandProducts } from 'store/HomePage/actions';

const PopularTab = props => {
    const [pageId, updatePageId] = useState(2)
    const dispatch = useDispatch()
    const {
        productList, tabType
    } = props

    const settings = {
        dots: false,
        arrows: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        autoplay: false,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
        afterChange: function(index) {
            if (index % 3 === 0) {
                new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ pageId: pageId, tabType, device: 'mobile', resolve, reject })));
                updatePageId(pageId + 1);
            }
          }
    };


    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+'
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    return (
        <Slider {...settings}>
            {
                productList?.map((product, index) => {
                    return (
                        <div className="m-card" key={index}>
                            <div className={`m-card__heading colbg${index + 1}`}>
                                {/* <span className="m-flag-yellow">BESTSELLER</span> */}
                                {product.tags === 2 && <span className="m-flag-blue">NEW</span>}
                                {product.tags === 1 && <span className="m-flag-yellow">BESTSELLER</span>}
                                <figure>
                                    <img src={product.imgUrl} alt={product.imageAlt} itemProp="image" />
                                </figure>
                                <h3 className="m-heading3">
                                    <a href={`${siteDomain}${product.url}`} itemProp="url"> {product?.name?.length > 25 ? product?.name?.slice(0, 25) + '...' : product?.name} </a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating mt-5">
                                    <span className="m-rating">
                                        {product.stars?.map((star, index) => starRatings(star, index))}
                                        <span>{product.rating?.toFixed(1)}/5</span>
                                    </span>
                                    {/* <span className="m-mode">Online</span> */}
                                    {product.mode ? <span className="m-mode">{product.mode}</span> : ''}
                                </div>
                                <div className="m-card__duration-mode mt-10">
                                    {product.jobsAvailable ? <> <strong>{product.jobsAvailable}</strong> Jobs available </> : ''} {product.jobsAvailable && product.duration ? '|' : ''} {product.duration ? <>Duration: <strong>{product.duration} days</strong> </> : ''}
                                </div>
                                <a className="m-view-program mt-10" href={`${siteDomain}${product.url}`}>View program</a>
                            </div>
                        </div>
                    )
                })
            }
        </Slider>
    )
}

export default PopularTab;