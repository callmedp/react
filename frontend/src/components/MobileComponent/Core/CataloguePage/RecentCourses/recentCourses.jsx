import React, { Component }  from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './recentCourses.scss'
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';

const RecentCourses = (props) => {
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
    const { recentCoursesList } = useSelector(store => store.recentCourses);
    
    const starRatings = (star, index) => {
        return (
            star === '*' ? 
                <em className="micon-fullstar" key={index}></em> : star === '+' ? 
                <em className="micon-halfstar" key={index}></em> : 
                <em className="micon-blankstar" key={index}></em>
        )
    }

    return(
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-courses m-recent-courses">
                <h2 className="m-heading2 text-center">Recently added courses</h2>
                <Slider {...settings}>
                {
                    recentCoursesList?.slice(0,4)?.map((course, index) => {
                        return (
                            <div className="m-card" key={index}>
                                <div className="m-card__heading">
                                    <figure>
                                        <img src={course.img} alt={course.img_alt} />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <a to={`${siteDomain}${course.url}`}>{course.name}</a>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">{course.provider}</span>
                                    <span className="m-rating">
                                        {course?.stars?.map((star, index) => starRatings(star, index))}
                                        <span>{course?.rating?.toFixed(1)}/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>{course?.price}/-</strong> 
                                    </div>
                                </div>
                            </div>
                        )
                    })
                }
                </Slider>
            </div>
        </section>
    )
}

export default RecentCourses;