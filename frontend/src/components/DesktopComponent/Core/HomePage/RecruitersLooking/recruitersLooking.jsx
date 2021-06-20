import React from 'react';
import './recruitersLooking.scss';
import { Link } from 'react-router-dom';
import Carousel from 'react-bootstrap/Carousel';
import { useSelector } from 'react-redux';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const RecruitersLooking = () => {
    const { recruiterList } = useSelector(store => store.footer)
    const sendLearningTracking = useLearningTracking();

    const trackRecruitersLooking = (name, indx) => {
        let name_joined = name.replace(/ /g, '_');

        MyGA.SendEvent('ln_new_homepage', 'ln_recruiter_course', ' ln_click_course', name_joined, '', false, true)

        sendLearningTracking({
            productId: '',
            event: `homepage_recruiters_looking_${name_joined}_${indx}_clicked`,
            pageTitle:'homepage',
            sectionPlacement:'recruiters_looking',
            eventCategory: name_joined,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    const getSlide = (recruiterSlide) => recruiterSlide.slice(0,12)?.map((skill, index) => {
        return (
            <li className="col-sm-3" key={index}>
            <Link to={skill?.skillUrl} onClick={() => trackRecruitersLooking(skill.skillName, index)}>
                <div className="card">
                    <figure>
                        <img src={skill.image} className="img-fluid" alt={skill.name} />
                    </figure>
                    <h3>{skill.skillName}</h3>
                    { !!skill.no_courses ? <strong>{skill.no_courses} { skill.no_courses == 1 ? 'course': 'courses'}</strong> : ''}
                    <Link>Know more</Link>
                </div>
            </Link>
            </li>
        )
    })

    return (
        <section className="container-fluid mt-0 mb-0" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="all-category mt-40 mb-30 pos-rel">
                        <h2 className="heading2 mb-0 text-center">What recruiters are looking at</h2>
                        <p className="text-center mt-5">Browse the skills with high demands to enhance your career</p>
                        <Carousel controls={ recruiterList?.length > 1 ? true : false }>
                            {
                                recruiterList?.map((recruiterSlide, inx) => {
                                    return (
                                        <Carousel.Item interval={10000000000} key={inx}>
                                            <ul className="all-category__list">
                                                {
                                                    getSlide(recruiterSlide)
                                                }
                                            </ul>
                                        </Carousel.Item>
                                    )
                                })
                            }
                        </Carousel>
                        {/* <span className="pink-circle2" data-aos="fade-right"></span>
                        <span className="pink-circle3" data-aos="fade-left"></span> */}
                    </div>
                </div>
            </div>
        </section>
    )
}

export default RecruitersLooking;