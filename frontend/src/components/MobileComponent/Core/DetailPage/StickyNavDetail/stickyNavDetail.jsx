import React from 'react';
import './stickyNavDetail.scss';
import {Link} from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';

const StickyNavDetail = (props) => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };
    return (
            <div className="m-sticky-detail m-container mt-0 mb-0 p-0" data-aos="fade-down">
                <div className="m-sticky-detail__price">
                    <strong className="mt-10 mb-10">3,499/- <del>5,499/-</del></strong>
                    <Link to={"#"} className="btn btn-secondary ml-auto">Enroll now</Link>
                </div>
                <div className="m-sticky-detail__nav">
                    <Slider {...settings}>
                        <Link className="active" to={"#"}>Key Features</Link>
                        <Link to={"#"}>Outline</Link>
                        <Link to={"#"}>Outcome</Link>
                        <Link to={"#"}>How to begin</Link>
                        <Link to={"#"}>FAQ</Link>
                        <Link to={"#"}>Reviews</Link>
                        <Link to={"#"}></Link>
                    </Slider>
                </div>
            </div>
    )
}

export default StickyNavDetail;