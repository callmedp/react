import React from 'react';
import { Link } from 'react-router-dom';
import './careerGuidance.scss';

const CareerGuidance = (props) => {
    return (
        <section className="m-container mt-0 mb-0 m-career-guidance">
            Confused what to explore? <Link for="#">Get Career Guidance</Link>
        </section>
    )
}

export default CareerGuidance;