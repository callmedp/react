import React from 'react';
import { Link } from 'react-router-dom';
import './careerGuidance.scss';
import useLearningTracking from 'services/learningTracking';
import { MyGA } from 'utils/ga.tracking.js';

const CareerGuidance = () => {
    const sendLearningTracking = useLearningTracking();

    const goToCareerGuidance = () => {
        MyGA.SendEvent('ln_career_guidance','ln_career_guidance', 'ln_click_career_guidance', 'career_guidance','', false, true);
        
        sendLearningTracking({
            productId: '',
            event: 'homepage_banner_career_guidance_clicked',
            pageTitle:'homepage',
            sectionPlacement: 'banner_career_guidance',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section className="m-container mt-0 mb-0 m-career-guidance">
            Confused what to explore? <Link to={'/user-intent'} onClick={() => goToCareerGuidance()} htmlFor="#">Get Career Guidance</Link>
        </section>
    )
}

export default CareerGuidance;