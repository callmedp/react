import React from 'react';
import Slider from "react-slick";
import './upgradeSkills.scss'

const UpgradeSkills = () => {
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
    
    return(
        <section className="m-container mt-0 mb-0 pr-0 pt-0 ml-10n">
            <div className="m-upgrade-skills">
                <h2 className="m-heading2-home text-center mb-5">Why upgrade your skills </h2>
                <p className="fs-13 text-center">Top reasons to upgrade your skills</p>
                <Slider {...settings}>
                    <div className="m-upgrade-skills__list">
                        <figure className="micon-become-expert1"></figure> 
                        <p>Become an expert and get ready for the future </p>
                    </div>
                    <div className="m-upgrade-skills__list">
                        <figure className="micon-become-expert2"></figure> 
                        <p>To reach the next step in your career ladder</p>
                    </div>
                    <div className="m-upgrade-skills__list">
                        <figure className="micon-become-expert3"></figure> 
                        <p>Create a brand for yourself, to differentiate</p>
                    </div>
                </Slider>
            </div>
        </section>
    )
}

export default UpgradeSkills;