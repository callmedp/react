// React Core Import
import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

// Third-Party Import
import Slider from "react-slick";

// Inter-App Import
import './recruitersLooking.scss';

const RecruitersLooking = () => {
    const { trendingSkills } = useSelector(store => store?.skillDemand);
    const sendLearningTracking = useLearningTracking();

    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        // centerMode: true,
        variableWidth: true,
        variableHeight: true,
    };

    const trackRecruitersLooking = (name, indx) => {
        MyGA.SendEvent('ln_new_homepage', 'ln_recruiter_course', ' ln_click_course', stringReplace(name), '', false, true)

        sendLearningTracking({
            productId: '',
            event: `homepage_recruiters_looking_${stringReplace(name)}_${indx}_clicked`,
            pageTitle:'homepage',
            sectionPlacement:'recruiters_looking',
            eventCategory: stringReplace(name),
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0 pb-0 pr-0 ml-10n" data-aos="fade-up">
            <div className="m-recruiters-looking">
                <h2 className="m-heading2-home text-center mb-5">What recruiters are looking at</h2>
                <p className="fs-13 text-center">Browse the skills with high demands</p>
                <Slider {...settings}>

                    {
                        trendingSkills?.slice(0,12)?.map((skill, index) => {
                            return (
                                <Link to={skill.skillUrl} key={index} onClick={() => trackRecruitersLooking(skill.skillName, index)}>
                                <div className="m-card" >
                                    
                                    <figure>
                                        <img src={`${skill?.image}`} className="img-fluid" alt={skill?.skillName} />
                                    </figure>
                                    <h3>{skill?.skillName}</h3>
                                    { !!skill.no_courses ? <span>{skill.no_courses} { skill.no_courses == 1 ? 'course': 'courses'}</span> : ''}
                                    <em>Know more</em>
                                    
                                </div>
                                </Link>
                            )
                        })
                    }
                </Slider>
            </div>
        </section>
    )
}

export default RecruitersLooking;