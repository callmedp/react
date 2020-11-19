import React from 'react';
import './whoLearn.scss'
import {  useSelector } from 'react-redux';

const WhoLearn = (props) => {

    const { whoShouldLearn } =  useSelector( store => store.skillBanner )

    return (
        <section className="container">
            <div className="row">
                <div className="who-learn">
                    <h2 className="heading2">Who should learn?</h2>
                    <p dangerouslySetInnerHTML={{__html : whoShouldLearn?.description}}>
                        </p>
                    
                    {/* <ul>
                        <li>People willing to learn and grow digital marketing from a realistic point of view</li>
                        <li>Professional willing to grow and evolve in marketing or related fields</li>
                        <li>Candidates who want to learn and improve marketing skills</li>
                        <li>People who wish for an exciting career in the exciting and fast-moving worlds of digital marketing</li>
                        <li>Young professionals who wish to gain a deeper understanding of internet marketing</li>
                    </ul> */}
                </div>
            </div>
        </section>
    )
}


export default WhoLearn;