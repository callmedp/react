import React from 'react';
import './banner.scss';

export default function Banner() {
    return(
        <div className="banner">
            <div className="container-box">
                <h1 className="mb-20"><span>Hello Sachin <br/>Your resume scored 70 out of 100</span></h1>
                
                <div className="banner__image">
                    <img src="/media/images/score-bg.png" alt=""/>
                </div>


                <div class="circle"></div>
                    <div class="dots"></div>
            </div>
        </div>
    );
} 