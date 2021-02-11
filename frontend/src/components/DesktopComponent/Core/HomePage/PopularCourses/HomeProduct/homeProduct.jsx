import React, { useState } from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import { useDispatch } from "react-redux";
import { fetchInDemandProducts } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';
import { siteDomain } from 'utils/domains';

const HomeProduct = (props) => {

    const [index, setIndex] = useState(0);
    const { tabType, popularProducts } = props;
    const dispatch = useDispatch()


    const handleSelect = async (selectedIndex, e) => {
        if (e !== undefined) {
            if (popularProducts.length === 0 || popularProducts[selectedIndex].length === 0) {
                dispatch(startHomePageLoader())
                await new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ pageId: selectedIndex + 1, tabType, device: 'desktop', resolve, reject })));
                dispatch(stopHomePageLoader())
            }
            setIndex(selectedIndex);
        }
    };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }
   



    return (
        <Carousel className="" fade={true} activeIndex={index} onSelect={handleSelect} >
            {
                popularProducts?.map((productList, indx) => {
                    return (
                        <Carousel.Item interval={10000000000} key={indx}>
                            <ul className="courses-tray__list">
                                {
                                    productList.map((product, idx) => {
                                        return (
                                            <li className="col-sm-3" key={product.id}>
                                                <div className="card">
                                                    <div className={`card__heading colbg${idx+1}`}>
                                                        {product.tags === 2 && <span className="flag-blue">NEW</span>}
                                                        {product.tags === 1 && <span className="flag-yellow">BESTSELLER</span>}
                                                        <figure>
                                                            <img src={product.imgUrl} alt={product.imageAlt} itemProp="image" />
                                                        </figure>
                                                        <h3 className="heading3">
                                                            <a itemProp="url" href={`${siteDomain}${product.url}`} >{product.name}</a>
                                                        </h3>
                                                    </div>
                                                    <div className="card__box">
                                                        <div className="card__rating mt-5">
                                                            <span className="rating">
                                                                {product.stars?.map((star, index) => starRatings(star, index))}
                                                                <span>{product.rating?.toFixed(1)}/5</span>
                                                            </span>
                                                            {product.mode ? <span className="mode">{product.mode}</span> : ''}
                                                        </div>
                                                        <div className="card__duration-mode mt-10">
                                                            {product.jobsAvailable ? <> <strong>{product.jobsAvailable}</strong> Jobs available </> : ''} {product.jobsAvailable && product.duration ? '|' : ''} {product.duration ? <>Duration: <strong>{product.duration} days</strong> </> : ''}
                                                        </div>
                                                        <a className="view-program mt-10" href={`${siteDomain}${product.url}`}>View program</a>
                                                    </div>
                                                </div>
                                            </li>
                                        )
                                    })
                                }
                            </ul>
                        </Carousel.Item>
                    )
                })
            }
        </Carousel>
    )
}

export default HomeProduct;