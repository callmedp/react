import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'
import { siteDomain, resumeShineSiteDomain } from 'utils/domains';

const CTAhome = (props) => {
    return(
        <section className="m-container m-cta m-cta-home" data-aos="fade-up">
            <Link to='/online-courses.html'>
                <figure className="micon-courses"></figure>
                Courses
            </Link>
            <a href={`${siteDomain}/practice-tests/`}>
                <figure className="micon-practice-test"></figure>
                Practice Test
            </a>
            <a href={`${siteDomain}/talenteconomy/`}>
                <figure className="micon-blogs"></figure>
                Blogs
            </a>
            <a href={`${resumeShineSiteDomain}`}>
                <figure className="micon-services"></figure>
                Services
            </a>
        </section>
    )
}

export default CTAhome;