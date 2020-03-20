import React, { useState } from 'react';
import Banner from './Banner/banner.jsx';
import Benefits from './Benefits/benefits.jsx';
import Features from './Features/features.jsx';
import GetExperts from './GetExperts/getExperts.jsx';
import ImproveScore from './ImproveScore/improveScore.jsx';
import Navbar from './Navbar/navbar.jsx';
import Footer from '../../Common/Footer/footer.jsx'
// import ResumeCheckerParameter from './ResumeCheckerParameters/resumeCheckerParameters.jsx'
// import ResumeCheckerWorks from './ResumeCheckerWorks/resumeCheckerWorks.jsx'
// import NextBenefit from './nextBenefit/nextBenefit.jsx';


export default function Home(){
    return (
    <div>
        <Navbar></Navbar>
        <Banner></Banner>
        <Features></Features>
        <GetExperts></GetExperts>
        <ImproveScore></ImproveScore>
        <Benefits></Benefits>
        <Footer></Footer>
    </div>
    );
}