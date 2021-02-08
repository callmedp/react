import React, { Component } from "react";
import { useSelector } from 'react-redux';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import '../../SkillPage/LearnersStories/learnersStories.scss';
import './boostedCareers.scss'
import LearnersStoriesCards from '../../../Common/LearnersStoriesCards/learnersStoriesCards'

const BoostedCareers = (props) => {
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
    
    const { testimonialCategory } = useSelector(store => store.testimonials)
    
    return (
        testimonialCategory?.length ? <LearnersStoriesCards learnersData = {testimonialCategory} page="homePage" /> : ''
    ) 

    // return (
    // <section className="m-container mt-0 mb-0 pb-0 pr-0" data-aos="fade-up">
    //     <h2 className="m-heading2-home mb-10 w-70 text-center mx-auto">See how they boosted their careers</h2>
    //     <div className="m-learner-stories ml-10n">
    //         <Slider {...settings}>
    //             <div className="m-card text-center">
    //                 <span className="m-card__name">AS</span>
    //                 <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
    //                 <strong>Abhishek Sinha</strong>
    //                 <span className="m-card__location">Sapient, Noida</span>
    //             </div>
    //             <div className="m-card text-center">
    //                 <span className="m-card__name">GS</span>
    //                 <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
    //                 <strong>Gaurav Singh</strong>
    //                 <span className="m-card__location">Sapient, Noida</span>
    //             </div>
    //             <div className="m-card text-center">
    //                 <span className="m-card__name">SS</span>
    //                 <p className="m-card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
    //                 <strong>Shruti Sharma</strong>
    //                 <span className="m-card__location">Sapient, Noida</span>
    //             </div>
    //         </Slider>
    //     </div>
    // </section>
    // );
  }

export default BoostedCareers;