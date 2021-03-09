import React from 'react';
import './takeFreeTest.scss';
import { Link } from 'react-router-dom';

const TakeFreeTest = (props) => {
    
    return (
        <section className="container-fluid" data-aos="fade-up">
            <div className="row">
                <div className="take-test-free">
                    <strong>Test your skills</strong>
                    <p>Take our free practice test to test your skill level in <strong>Digital Marketing</strong></p>
                    <Link to={"#"} className="btn btn-outline-primary">Take free test</Link>
                </div>
            </div>
        </section>
    )
}

export default TakeFreeTest;