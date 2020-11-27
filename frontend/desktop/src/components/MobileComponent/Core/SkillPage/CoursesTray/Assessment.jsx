import React, { Component } from "react";
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import './courses.scss';

const Assessment = (props) => {
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
    return (
    <section className="m-container mt-0 mb-0 pb-0">
        <h2 className="m-heading2 mb-10">Assessment for you</h2>
        <div className="m-courses m-courses-slider ml-10n">
            <Slider {...settings}>
                <div className="m-card">
                    <div className="m-card__heading">
                        <span className="m-flag-blue">NEW</span>
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h3 className="m-heading3">
                            <Link to={"#"}>Digital Marketing Training Course</Link>
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
                        <div className="m-card__duration-mode">
                            Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                        </div>
                        <div className="m-card__price">
                            <strong>12999/-</strong> 
                        </div>
                    </div>
                    <div className="m-card__popover">
                        <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                         <strong> 2819</strong> Jobs available
                        </p>
                        <p>
                            <strong>About</strong>
                            This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                        </p>
                        <p>
                            <strong>Skills you gain</strong>
                            Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                        </p>
                        <p>
                            <strong>Highlights</strong>
                            <ul>
                                <li>Anytime and anywhere access</li>
                                <li>Become a part of Job centre</li>
                                <li>Lifetime course access</li>
                                <li>Access to online e-learning</li>
                            </ul>
                        </p>
                        <p className="d-flex align-items-center">
                            <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                            <Link to={"#"} className="micon-pdf ml-auto"></Link>
                        </p>
                    </div>
                </div>
                <div className="m-card">
                    <div className="m-card__heading">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h3 className="m-heading3">
                            <Link to={"#"}>Email Marketing Master Training Course</Link>
                        </h3>
                    </div>
                    <div className="m-card__box">
                        <div className="m-card__rating">
                        <span className="mr-10">By ERB</span>
                        <span className="m-rating">
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-blankstar"></em>
                            <span>4/5</span>
                        </span>
                        </div>
                        <div className="m-card__duration-mode">
                            Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                        </div>
                        <div className="m-card__price">
                            <strong>12999/-</strong> 
                            <Link to={"#"} className="m-icon-pdf"></Link>
                        </div>
                    </div>
                    <div className="m-card__popover">
                        <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                         <strong> 2819</strong> Jobs available
                        </p>
                        <p>
                            <strong>About</strong>
                            This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                        </p>
                        <p>
                            <strong>Skills you gain</strong>
                            Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                        </p>
                        <p>
                            <strong>Highlights</strong>
                            <ul>
                                <li>Anytime and anywhere access</li>
                                <li>Become a part of Job centre</li>
                                <li>Lifetime course access</li>
                                <li>Access to online e-learning</li>
                            </ul>
                        </p>
                        <p className="d-flex align-items-center">
                            <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                            <Link to={"#"} className="micon-pdf ml-auto"></Link>
                        </p>
                    </div>
                </div>
                <div className="m-card">
                    <div className="m-card__heading">
                        <span className="m-flag-red">BESTSELLER</span>
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h3 className="m-heading3">
                            <Link to={"#"}>Digital Marketing Training Course</Link>
                        </h3>
                    </div>
                    <div className="m-card__box">
                        <div className="m-card__rating">
                        <span className="mr-10">By ERB</span>
                        <span className="m-rating">
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-fullstar"></em>
                            <em className="m-icon-blankstar"></em>
                            <span>4/5</span>
                        </span>
                        </div>
                        <div className="m-card__duration-mode">
                            Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                        </div>
                        <div className="m-card__price">
                            <strong>12999/-</strong> 
                            <Link to={"#"} className="m-icon-pdf"></Link>
                        </div>
                    </div>
                    <div className="m-card__popover">
                        <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                         <strong> 2819</strong> Jobs available
                        </p>
                        <p>
                            <strong>About</strong>
                            This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                        </p>
                        <p>
                            <strong>Skills you gain</strong>
                            Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                        </p>
                        <p>
                            <strong>Highlights</strong>
                            <ul>
                                <li>Anytime and anywhere access</li>
                                <li>Become a part of Job centre</li>
                                <li>Lifetime course access</li>
                                <li>Access to online e-learning</li>
                            </ul>
                        </p>
                        <p className="d-flex align-items-center">
                            <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                            <Link to={"#"} className="micon-pdf ml-auto"></Link>
                        </p>
                    </div>
                </div>
            </Slider>
        </div>

        {/* assessment list */}
        <h2 className="m-heading2 mt-20 mb-20">More assessment</h2>
        <div className="m-courses">
            <div className="m-card">
                <div className="m-card__heading">
                    <span className="m-flag-blue">NEW</span>
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
                    <div className="m-card__duration-mode">
                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                    </div>
                    <div className="m-card__price">
                        <strong>12999/-</strong> 
                        <Link to={"#"} className="m-view-more">View more</Link>
                    </div>
                </div>
            </div>
            <div className="m-card">
                <div className="m-card__heading">
                    <figure>
                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                    </figure>
                    <h3 className="m-heading3">
                        <Link to={"#"}>Email Marketing Master Training Course</Link>
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
                    <div className="m-card__duration-mode">
                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                    </div>
                    <div className="m-card__price">
                        <strong>12999/-</strong> 
                    </div>
                </div>
                <div className="m-card__popover">
                    <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                        <strong> 2819</strong> Jobs available
                    </p>
                    <p>
                        <strong>About</strong>
                        This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                    </p>
                    <p>
                        <strong>Skills you gain</strong>
                        Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                    </p>
                    <p>
                        <strong>Highlights</strong>
                        <ul>
                            <li>Anytime and anywhere access</li>
                            <li>Become a part of Job centre</li>
                            <li>Lifetime course access</li>
                            <li>Access to online e-learning</li>
                        </ul>
                    </p>
                    <p className="d-flex align-items-center">
                        <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                        <Link to={"#"} className="micon-pdf ml-auto"></Link>
                    </p>
                    <Link to={"#"} className="m-view-less d-block text-right">View less</Link>
                </div>
            </div>
            <div className="m-card">
                <div className="m-card__heading">
                    <span className="m-flag-red">BESTSELLER</span>
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
                    <div className="m-card__duration-mode">
                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                    </div>
                    <div className="m-card__price">
                        <strong>12999/-</strong> 
                        <Link to={"#"} className="m-view-more">View more</Link>
                    </div>
                </div>
            </div>
        </div>
    </section>
    );
  }

export default Assessment;