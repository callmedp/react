import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import './popularCourses.scss';

const PopularCourses = (props) => {
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
        <section className="m-container mt-0 mb-0 pr-0 pt-20">
            <div className="m-courses m-popular-course-demand">
                <h2 className="m-heading2-home text-center">Popular courses in demand</h2>

                <div className="m-tabset-pop">
                    <input type="radio" name="tabset" id="tab1" aria-controls="Master’s" defaultChecked={true} />
                    <label htmlFor="tab1">Master’s</label>

                    <input type="radio" name="tabset" id="tab2" aria-controls="Certifications" />
                    <label htmlFor="tab2">Certifications</label>

                    <div className="tab-panels">
                        <div id="tab1" className="tab-panel">
                            <div className="m-courses">
                                <Slider {...settings}>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg1">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg2">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div> 
                                    <div className="m-card">
                                        <div className="m-card__heading colbg3">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg4">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </Slider>
                            </div>
                        </div>
                        <div id="tab2" className="tab-panel">
                        <div className="m-courses">
                                <Slider {...settings}>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg1">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>2 Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg2">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div> 
                                    <div className="m-card">
                                        <div className="m-card__heading colbg3">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg4">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
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
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                </Slider>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </section>
    )
}
   
export default PopularCourses;