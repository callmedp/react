import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './recommendedCourses.scss';

const RecommendedCourses = (props) => {
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
    return(
        <section className="m-container mt-0 mb-0">
            <div className="m-recomend-courses">
                <h2 className="m-heading2 text-center">Recommended Courses</h2>
                <Slider {...settings}>
                    <div className="m-recomend-courses__tab">
                        <a className="selected" href="#">Sales and Marketing</a>
                    </div>
                    <div className="m-recomend-courses__tab">
                        <a href="#">Information Technology</a>
                    </div>
                    <div className="m-recomend-courses__tab">
                        <a href="#">Banking & Finance</a>
                    </div>  
                </Slider>
                <div className="m-courses m-recent-courses">
                    <Slider {...settings}>
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
                                <span className="mr-10">By ERB</span>
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
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
                                <span className="mr-10">By ERB</span>
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                </div>
                            </div>
                        </div>  
                    </Slider>
                </div>
            </div>
        </section>
    )
}
   
export default RecommendedCourses;