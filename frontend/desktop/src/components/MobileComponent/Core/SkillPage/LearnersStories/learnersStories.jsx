import React, { Component } from "react";
import Slider from "react-slick";
import './learnersStories.scss';

const LearnersStories = (props) => {
    const settings = {
      dots: false,
      infinite: true,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1
    };
    return (
    <section className="m-container">
        <h2 className="m-heading2 m-auto pb-20">Learners stories</h2>
        <div className="m-learner-stories">
            <Slider {...settings}>
                <div className="m-card text-center">
                    <span className="m-card__name">AS</span>
                    <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                    <strong>Abhishek Sinha</strong>
                    <span className="m-card__location">Sapient, Noida</span>
                </div>
                <div className="m-card text-center">
                    <span className="m-card__name">GS</span>
                    <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                    <strong>Gaurav Singh</strong>
                    <span className="m-card__location">Sapient, Noida</span>
                </div>
                <div className="m-card text-center">
                    <span className="m-card__name">SS</span>
                    <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                    <strong>Shruti Sharma</strong>
                    <span className="m-card__location">Sapient, Noida</span>
                </div>
            </Slider>
        </div>
    </section>
    );
  }

export default LearnersStories;