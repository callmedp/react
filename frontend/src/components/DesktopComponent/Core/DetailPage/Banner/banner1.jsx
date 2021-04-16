import React from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import {Link} from 'react-router-dom';

const BannerCourseDetail1 = (props) => {

    return (
       <header className="container-fluid pos-rel course-detail-bg">
            <div className="row">
                <div className="container detail-header-content">
                    <div className="w-65">
                        <Breadcrumb>
                            <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
                            <Breadcrumb.Item href="#">
                                Automated Manual Testing
                            </Breadcrumb.Item>
                            <Breadcrumb.Item active>Digital Marketing</Breadcrumb.Item>
                        </Breadcrumb>
                        <div className="detail-heading mt-40" data-aos="fade-right">
                            <div className="detail-heading__icon">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                            </div>
                            <div className="detail-heading__content">
                                <span className="flag-yellowB">BESTSELLER</span>
                                <h1 className="heading1">
                                    Automated Manual Testing
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
                        <ul className="course-stats mt-40 mb-20">
                            <li>
                                <strong>By Simplilearn</strong> <Link to={"#"}>View all</Link> courses by Simplilearn  
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-course-duration mr-10"></figure>
                                <p>
                                    Course Duration <strong>3 Hrs.</strong>
                                </p>
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-question-no mr-10"></figure>
                                <p>
                                No. of questions <strong>50</strong>
                                </p>
                            </li>
                        </ul>
                        <div className="intro-video mt-40">
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
                                <strong className="price-taxes mt-20 mb-10">3,499/- <span className="taxes">(+taxes)</span></strong>
                                <p className="d-flex mb-0">
                                    <Link to={"#"} className="btn btn-secondary mt-10 mb-30 mr-10">Enroll now</Link>
                                    <Link to={"#"} className="btn btn-outline-primary mb-30 mt-10">Enquire now</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
       </header> 
    )
}

export default BannerCourseDetail1;