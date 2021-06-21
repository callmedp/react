// React Core Import
import React from 'react';
import { useSelector } from 'react-redux';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

// Third-Party Import
import Slider from "react-slick";

// Inter-App Import
import './servicesForYou.scss'
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';

const ServicesForYou = () => {
    const { jobAssistanceServices } = useSelector(store => store?.jobAssistance)
    const sendLearningTracking = useLearningTracking();

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

    const goToAssistedService = (heading, indx) => {

        MyGA.SendEvent('ln_new_homepage','ln_assistance_services_select', 'ln_click_assistance_services', stringReplace(heading), '', false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_assistance_service_${stringReplace(heading)}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'service_for_you',
            eventCategory: stringReplace(heading),
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <section className="m-container mt-0 mb-0 pr-0 ml-10n" data-aos="fade-up">
            <div className="m-services-foryou">
                <h2 className="m-heading2-home text-center mb-5">Job assistance services</h2>
                <p className="fs-13 text-center">Find your next job faster by using our services</p>
                <Slider {...settings}>

                    {
                        jobAssistanceServices?.map((job, index) => {
                            return (
                                <a href={`${siteDomain}${job?.url}`} onClick={() => goToAssistedService(job?.heading, index)} key={index}>
                                <div className="m-services-foryou__list">
                                    <h3 className="m-heading3">{ job?.heading }</h3>
                                    <p>{ job?.description?.length > 80 ? job?.description?.slice(0, 80) + '...' : job?.description }</p>
                                    <span className="d-flex">
                                        <a>Know more</a>
                                        {/* <figure className={`micon-service${index + 1}`}></figure> */}
                                        <figure>
                                            <img src={job?.img} />
                                        </figure>
                                    </span>
                                </div>
                                </a>
                            )
                        })
                    }
                </Slider>
            </div>
        </section>
    )
}

export default ServicesForYou;