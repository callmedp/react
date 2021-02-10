import React from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import './cta.scss'

const CTAhome = (props) => {
    return(
        <section className="m-container m-cta m-cta-home" data-aos="fade-up">
            <Link to={"#"}>
                <figure className="micon-courses"></figure>
                Courses
            </Link>
            <Link to={"#"}>
                <figure className="micon-practice-test"></figure>
                Practice Test
            </Link>
            <Link to={"#"}>
                <figure className="micon-blogs"></figure>
                Blogs
            </Link>
            <Link to={"#"}>
                <figure className="micon-services"></figure>
                Services
            </Link>
        </section>
    )
}

export default CTAhome;