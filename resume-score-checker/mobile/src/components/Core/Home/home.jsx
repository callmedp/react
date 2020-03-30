import React from 'react';
import Header from '../../Common/Header/header';
import Banner from './Banner/banner';
import Features from './Features/features';
import HowItWorks from './HowItWorks/howItWork';
import Parameters from './ResumeCheckerParameters/resumeCheckerParameters';
import NextBenefit from './NextBenefit/nextBenefit';
import CallToAction from './CallToAction/callToAction';
import Footer from '../../Common/Footer/footer';
import './home.scss';


export default function Home(){
    return (
        <div className="body-wrapper">
            {
                <div className="h-100">
                    <Header/>
                    <Banner/>
                    <Features/>
                    <HowItWorks/>
                    <Parameters/>
                    <NextBenefit/>
                    <CallToAction/>
                    <Footer/>
                </div>
            }
        </div>
    );
}