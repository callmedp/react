import React, { useState } from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from "react-redux";
import { fetchInDemandProducts } from 'store/HomePage/actions';


const HomeProduct = (props) => {

    const [index, setIndex] = useState(0);
    const { tabType, popularProducts } = props;
    const dispatch = useDispatch()

    const handleSelect = (selectedIndex, e) => {
        if (popularProducts[selectedIndex].length === 0) {
            new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ pageId: selectedIndex, tabType, device: 'desktop', resolve, reject })));
        }
        setIndex(selectedIndex);
    };

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
                                                    <div className="card__heading colbg1">
                                                        <span className="flag-yellow">BESTSELLER</span>
                                                        <figure>
                                                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                                        </figure>
                                                        <h3 className="heading3">
                                                            <Link to={"#"}>Digital Marketing Training Course</Link>
                                                        </h3>
                                                    </div>
                                                    <div className="card__box">
                                                        <div className="card__rating mt-5">
                                                            <span className="rating">
                                                                <em className="icon-fullstar"></em>
                                                                <em className="icon-fullstar"></em>
                                                                <em className="icon-fullstar"></em>
                                                                <em className="icon-fullstar"></em>
                                                                <em className="icon-blankstar"></em>
                                                                <span>4/5</span>
                                                            </span>
                                                            <span className="mode">Online</span>
                                                        </div>
                                                        <div className="card__duration-mode mt-10">
                                                            <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                                        </div>
                                                        <Link className="view-program mt-10" to={"#"}>View program</Link>
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