import React, { useState } from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';


const HomeProduct = (props) =>{

    const [index, setIndex] = useState(0);

    const handleSelect = (selectedIndex, e) => {
    setIndex(selectedIndex);
    };

    const product = [1,2,3,4]
    const carArray = [1,2,3]

    return (
        <Carousel className=""  activeIndex={index} onSelect={handleSelect}>
                        {
                            carArray.map((lii, ind) => {
                                return (
                                    <Carousel.Item interval={10000000000}>
                            <ul className="courses-tray__list">
                              {
                                  product.map((item, index) => {
                                      return (
                                        <li className="col-sm-3">
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