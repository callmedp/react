import React, { useState } from 'react';
import './recruitersLooking.scss';
import { Link } from 'react-router-dom';
import Carousel from 'react-bootstrap/Carousel';
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';

const RecruitersLooking = (props) => {


    const { recruiterList } = useSelector(store => store.footer)
    

    const getSlide = (recruiterSlide) => recruiterSlide?.map((skill, index) => {
        return (
            <li className="col-sm-3">
                <div className="card">
                    <figure>
                        <img src={skill.image} className="img-fluid" alt={skill.name} />
                    </figure>
                    <h3>{skill.skillName}</h3>
                    { !!skill.no_courses ? <strong>{skill.no_courses} { skill.no_courses == 1 ? 'course': 'courses'}</strong> : ''}
                    <Link to={skill.skillUrl}>Know more</Link>
                </div>
            </li>
        )
    })

    return (
        <section className="container-fluid mt-0 mb-0" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="all-category mt-40 mb-30 pos-rel">
                        <h2 className="heading2 mb-5 text-center">What recruiters are looking at</h2>
                        <p className="text-center">Browse the skills with high demands to enhance your career</p>
                        <Carousel>
                            {
                                recruiterList?.map((recruiterSlide, inx) => {
                                    return (
                                        <Carousel.Item interval={10000000000}>
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