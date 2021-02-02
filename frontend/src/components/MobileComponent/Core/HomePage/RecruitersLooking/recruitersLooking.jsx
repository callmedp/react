// React Core Import
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

// Third-Party Import
import Swal from 'sweetalert2';
import Slider from "react-slick";

// Inter-App Import
import './recruitersLooking.scss';
import 'slick-carousel/slick/slick.css';

// API Import
import { fetchSkillwithDemands } from 'store/HomePage/actions';

   
const RecruitersLooking = (props) => {
    const dispatch = useDispatch();

    const { trendingSkills } = useSelector(store => { console.log(store); return store?.skillDemand });

    const settings = {
        dots: false,
        arrows: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        centerMode: true,
        variableWidth: true,
        variableHeight: true,
    };


    const handleEffects = async () => {
        try{
            if (!(window && window.config && window.config.isServerRendered)) {
                await new Promise((resolve, reject) => dispatch(fetchSkillwithDemands({ resolve, reject })));
            }
            else {
                delete window.config?.isServerRendered
            }
        }
        catch(e){
            Swal.fire({
                icon: 'error',
                text: 'Sorry! we are load data from server.'
            })
        }
    };


    useEffect( () => {
        handleEffects();
    }, [])

    console.log(trendingSkills)

    return(
        <section className="m-container m-lightblue-bg mt-0 mb-0 pb-0 pl-0 pr-0" data-aos="fade-up">
            <div className="m-all-category">
                <h2 className="m-heading2-home text-center mb-5">What recruiters are looking at</h2>
                <p className="fs-13 text-center">Browse the skills with high demands</p>
                <Slider {...settings}>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories1.jpg" className="img-fluid" alt="Personal Development" />
                        </figure>
                        <h3>Personal Development</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories2.jpg" className="img-fluid" alt="Information Technology" />
                        </figure>
                        <h3>Information Technology</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories3.jpg" className="img-fluid" alt="Sales and Marketing" />
                        </figure>
                        <h3>Sales and Marketing</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories4.jpg" className="img-fluid" alt="Human Resources (HR)" />
                        </figure>
                        <h3>Human Resources (HR)</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories5.jpg" className="img-fluid" alt="Management" />
                        </figure>
                        <h3>Management</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories6.jpg" className="img-fluid" alt="Law" />
                        </figure>
                        <h3>Law</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories7.jpg" className="img-fluid" alt="Operation Management" />
                        </figure>
                        <h3>Operation Management</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                    <div className="m-card">
                        <figure>
                            <img src="./media/images/mobile/categories8.jpg" className="img-fluid" alt="Mass Communication" />
                        </figure>
                        <h3>Mass Communication</h3>
                        <span>30 courses</span>
                        <Link to={"#"}>Know more</Link>
                    </div>
                </Slider>
            </div>
        </section>
    )
}
   
export default RecruitersLooking;