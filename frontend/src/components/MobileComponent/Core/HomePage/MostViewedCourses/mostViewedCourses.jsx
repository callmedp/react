import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './mostViewedCourses.scss';
import { categoryTabs } from 'utils/constants';
import { fetchMostViewedCourses } from 'store/HomePage/actions';
import ProductCardsSlider from '../../../Common/ProductCardsSlider/productCardsSlider';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions/index';

const MostViewedCourses = (props) => {
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

    const dispatch = useDispatch()
    const [selectedIndex, setSelectedIndex] = useState('-1')
    const { mostViewedCourses } = useSelector(store => store.mostViewed);

    const handleCategory = async tabType => {
        try {
            if (!mostViewedCourses[tabType] || mostViewedCourses[tabType].length === 0) {
                dispatch(startHomePageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ categoryId: tabType, resolve, reject })))
                dispatch(stopHomePageLoader());
            }
        }
        catch (e) {
            dispatch(stopHomePageLoader());
        }
        setSelectedIndex(tabType);
    }


    return (
        <section className="m-container mt-0 mb-0 m-lightblue-bg pr-0" data-aos="fade-up">
            <div className="m-recomend-courses">
                <h2 className="m-heading2-home text-center">Most Viewed Courses</h2>
                <Slider {...settings}>
                    {
                        categoryTabs?.map((category, index) => {
                            return (
                                <div className="m-recomend-courses__tab" key={category?.id} >
                                    <Link className={selectedIndex === category.id ? 'selected' : ''} to={'#'} onClick={() => handleCategory(category.id)}>{category?.name}</Link>
                                </div>
                            )
                        })
                    }
                    {/* <div className="m-recomend-courses__tab">
                        <Link className="selected" for={"#"}>All</Link>
                    </div>
                    <div className="m-recomend-courses__tab">
                        <Link for={"#"}>Sales and Marketing</Link>
                    </div>
                    <div className="m-recomend-courses__tab">
                        <Link for={"#"}>Information Technology</Link>
                    </div>
                    <div className="m-recomend-courses__tab">
                        <Link for={"#"}>Banking & Finance</Link>
                    </div>   */}
                </Slider>
                <div className="m-courses m-recent-courses">
                    {
                        <ProductCardsSlider productList={mostViewedCourses[selectedIndex]} noProvider={true} showMode={true} />
                    }
                    {/* <Slider {...settings}> 
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                <span className="m-mode">Online</span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                </div>
                            </div>
                        </div>
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                <span className="m-mode">Online</span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                </div>
                            </div>
                        </div>  
                    </Slider> */}
                </div>
            </div>
        </section>
    )
}

export default MostViewedCourses;