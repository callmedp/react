import React, { useState } from 'react';
import Banner from './Banner/banner';
import Features from './Features/features';
import HowItWorks from './HowItWorks/howItWork';
import Parameters from './ResumeCheckerParameters/resumeCheckerParameters';
import NextBenefit from './NextBenefit/nextBenefit';
import Footer from '../../Common/Footer/footer';
import './home.scss';


export default function Home(){
    return (

        <div className="body-wrapper">
            {
                <div className="h-100">
                    <Banner/>
                    <Features/>
                    <HowItWorks/>
                    <Parameters/>
                    <NextBenefit/>
                    <Footer/>
                </div>
            
            /* 
        <NextBenefit/>
        <ResumeCheckerWorks/>
        <ResumeCheckerParameter/> */}
    </div>
    );
}