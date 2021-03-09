import React from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import {Link} from 'react-router-dom';

const BannerCourseDetail = (props) => {

    return (
       <header className="container-fluid pos-rel course-detail-bg">
            <div className="row">
                <div className="container detail-header-content">
                    <div className="flex-1">
                        <Breadcrumb>
                            <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
                            <Breadcrumb.Item href="#">
                                Sales and Marketing
                            </Breadcrumb.Item>
                            <Breadcrumb.Item active>Digital Marketing</Breadcrumb.Item>
                        </Breadcrumb>
                        <div className="detail-heading" data-aos="fade-right">
                            <div className="detail-heading__icon">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                            </div>
                            <div className="detail-heading__content">
                                <span className="flag-yellowB">BESTSELLER</span>
                                <h1 className="heading1">
                                    Digital Marketing Master Training Course
                                </h1>
                                <div className="d-flex mt-15">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-halfstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    <span className="review-jobs">
                                        <Link to={"#"}>
                                            <figure className="icon-reviews-link"></figure> <strong>43</strong> Reviews
                                        </Link>
                                    </span>
                                    <span className="review-jobs">
                                        <Link to={"#"}>
                                            <figure className="icon-jobs-link"></figure> <strong>2819</strong> Jobs available
                                        </Link>
                                    </span>
                                </div>
                            </div>
                        </div>
                        <ul className="course-stats mt-30 mb-30">
                            <li>
                                <strong>By Simplilearn</strong> <Link to={"#"}>View all</Link> courses by Simplilearn  
                            </li>
                            <li>
                            <Link className="d-block" to={"#"}>+3 more</Link> Course providers  
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-course-duration mr-10"></figure>
                                <p>
                                    Course Duration <strong>180 Days</strong>
                                </p>
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-access-duration mr-10"></figure>
                                <p>
                                    Access Duration <strong>365 Days</strong>
                                </p>
                            </li>
                        </ul>
                        <div className="intro-video">
                            <figure className="intro-video__img">
                                <Link to={"#"}>
                                    <img src="/media/images/desktop/intro-video.jpg" alt="Intro Video" />
                                    <i className="icon-play-video"></i>
                                    <strong>Intro video</strong>
                                </Link>
                            </figure>
                            <p className="intro-video__content">This Course is intended for professionals and graduates wanting to excel in their chosen areas. It is also well suited for those who are already working and would like to take certification for further career progression. Earning Vskills Email Marketing Professional Certification. <Link to={"#"}>Read more</Link></p>
                        </div>
                    </div>
                    <div className="banner-detail">
                        <div className="course-enrol">
                            <div className="course-enrol__mode">
                                <form>
                                    Mode <label><input type="radio" value="" checked /> Online</label> 
                                    <label><input type="radio" value="" /> Class room</label>
                                </form>
                            </div>
                            <div className="course-enrol__price">
                                <strong className="mt-20 mb-10">3,499/- <del>5,499/-</del></strong>
                                <Link to={"#"} className="btn btn-secondary mt-10">Enroll now</Link>
                                <Link to={"#"} className="btn btn-outline-primary mt-10">Enquire now</Link>
                            </div>
                            <div className="course-enrol__offer lightblue-bg2">
                                <strong className="mt-10 mb-5">Offers</strong>
                                <ul className="pb-0">
                                    <li><figure className="icon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                                    <li><figure className="icon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                                    <li><figure className="icon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                                    <li><figure className="icon-offer-global"></figure> <strong>Global</strong> Education providers</li>
                                </ul>
                                <Link to={"#"}>+2 more</Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
       </header> 
    )
}

export default BannerCourseDetail;