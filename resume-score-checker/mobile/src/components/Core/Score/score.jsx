import React, { useState } from 'react';
import Footer from '../../Common/Footer/footer';
import Banner from './Banner/banner';
import './score.scss';



export default function Score(){
    return (

        <div className="body-wrapper">
            {
                <div className="h-100">
                   <Banner/>
                </div>
            }
    </div>
    );
}