import React from 'react';
import { Link } from 'react-router-dom';
import './Banner.scss';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import SearchPage from '../../../Common/SearchPage/SearchPage'

const HomeBanner = (props) => {
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
        <div className="m-container mt-0 mb-0 m-home-header">
            {/* <div className="m-top-search-header">
                <form id="searchForm" className="form-inline w-100 ml-auto">
                    <button className="m-btn-search-black d-flex align-items-center"><figure className="micon-search-black d-flex"></figure></button>
                    <input className="m-search-input" type="search" placeholder="Try Digital marketing certificate" name="query" id="transcript" aria-label="Search" autocomplete="off" />
                    <button className="m-btn-voice-search">
                        <figure className="micon-voice-search d-flex"></figure>
                    </button>
                </form>
            </div> */}
            <SearchPage crossSearch={false} placeholder="Try Digital marketing certificate"/>

            <div className="m-header-nav">
                <figure className="micon-home-nav"></figure>
                    <Slider {...settings}>
                        <Link to={"#"}>Sales</Link>
                         <Link to={"#"}>IT</Link> 
                         <Link to={"#"}>Finance</Link> 
                         <Link to={"#"}>Management</Link> 
                         <Link to={"#"}>Operations</Link> 
                    </Slider>
            </div>
        </div>
    )
}

export default HomeBanner;