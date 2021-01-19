import React from 'react';
import './whoLearn.scss'
import {  useSelector } from 'react-redux';

const WhoLearn = (props) => {

    const { whoShouldLearn } =  useSelector( store => store.skillBanner )

    return (
        <>
            {
                whoShouldLearn ?
                <section className="container">
                    <div className="row">
                        <div className="who-learn">
                            <h2 className="heading2">Who should learn?</h2>
                            <p dangerouslySetInnerHTML={{__html : whoShouldLearn }}></p>
                        </div>
                    </div>
                </section> : ''
            }
        </>
    )
}


export default WhoLearn;