import React, { useState } from 'react';
import Banner from './Banner/banner.jsx';
import Benefits from './Benefits/benefits.jsx';
import Features from './Features/features.jsx';
import Navbar from '../../Common/Navbar/navbar';
import Footer from '../../Common/Footer/footer.jsx';
import Parameters from './Parameters/parameters'
import HowItWorks from './HowItWorks/howItWorks.jsx';

export default function Home(){
    return (
    <div>
        <Navbar></Navbar>
        <Banner></Banner>
        <Features></Features>
        <HowItWorks></HowItWorks>
        <Parameters></Parameters>
        <Benefits></Benefits>
        <Footer></Footer>
    </div>
    );
}