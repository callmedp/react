import React from 'react';
import './whoLearn.scss'
import {  useSelector } from 'react-redux';

const WhoLearn = (props) => {
    const { whoShouldLearn } =  useSelector( store => store.skillBanner )

    return (
        <>
            { whoShouldLearn ?
                <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
                    <div className="m-who-learn">
                        <h2 className="m-heading2">Who should learn?</h2>
                        <p dangerouslySetInnerHTML={{__html : whoShouldLearn }}></p>
                    </div>
                </section> : ''
            }
        </>
    )
}


export default WhoLearn;