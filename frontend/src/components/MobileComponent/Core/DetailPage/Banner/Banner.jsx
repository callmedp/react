import React from 'react';
import {Link} from 'react-router-dom';
import './Banner.scss';

const CourseDetailBanner = (props) => {
    return (
        <div className="m-detail-header ml-15 mt-10">

            <div className="m-detail-heading">
                <div className="m-detail-heading__icon mt-30">
                    <figure>
                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                    </figure>
                </div>
                <div className="m-detail-heading__content">
                    <span className="m-flag-yellowB">BESTSELLER</span>
                    <h1 className="m-heading1 mt-5">
                        Digital Marketing Master Training Course
                    </h1>
                    <span className="m-rating">
                        <em className="micon-fullstar"></em>
                        <em className="micon-fullstar"></em>
                        <em className="micon-fullstar"></em>
                        <em className="micon-halfstar"></em>
                        <em className="micon-blankstar"></em>
                        <span>4/5</span>
                        <span>By Simplilearn</span>
                    </span>
                    <div className="d-flex mt-10">
                        
                        <span className="m-review-jobs">
                            <Link to={"#"}>
                                <figure className="micon-reviews-link"></figure> <strong>43</strong> Reviews
                            </Link>
                        </span>
                        <span className="m-review-jobs">
                            <Link to={"#"}>
                                <figure className="micon-jobs-link"></figure> <strong>2819</strong> Jobs available
                            </Link>
                        </span>
                    </div>
                    <ul className="m-course-stats mt-20 mb-20">
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
                </div>
            </div>
            <div className="m-intro-video">
                <figure className="m-intro-video__img">
                    <Link to={"#"}>
                        <img src="/media/images/mobile/intro-video.jpg" alt="Intro Video" />
                        <i className="micon-play-video"></i>
                    </Link>
                </figure>
                <p className="m-intro-video__content">This Course is intended for professionals and graduates wanting to excel in their chosen areas. It is also well suited for those who are already working. <Link to={"#"}>Read more</Link></p>
            </div>
            <ul className="m-course-stats mt-10 mb-10 bdr-top pt-20">
                <li>
                    <Link to={"#"}>View all</Link> courses by Simplilearn  
                </li>
                <li>
                <Link to={"#"}>+3 more</Link> Course providers  
                </li>
            </ul>
        </div>
    )
}

export default CourseDetailBanner;