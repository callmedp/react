import React from 'react';
import './whoLearn.scss'
import {  useSelector } from 'react-redux';

const WhoLearn = (props) => {
    const { whoShouldLearn } =  useSelector( store => store.skillBanner )

    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-who-learn">
                <h2 className="m-heading2">Who should learn?</h2>
                {/* <ul>
                    <li>People willing to learn and grow digital marketing from a realistic point of view</li>
                    <li>Professional willing to grow and evolve in marketing or related fields</li>
                    <li>Candidates who want to learn and improve marketing skills</li>
                    <li>People who wish for an exciting career in the exciting and fast-moving worlds of digital marketing</li>
                </ul> */}
                <p dangerouslySetInnerHTML={{__html : whoShouldLearn }}></p>
            </div>
        </section>
    )
}


export default WhoLearn;