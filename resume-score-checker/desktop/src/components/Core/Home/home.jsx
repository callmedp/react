import React from 'react';
import Banner from './Banner/banner.jsx';
import Benefits from './Benefits/benefits.jsx';
import Features from './Features/features.jsx';
import Navbar from '../../Common/Navbar/navbar';
import Footer from '../../Common/Footer/footer.jsx';
import Parameters from './Parameters/parameters'
import HowItWorks from './HowItWorks/howItWorks.jsx';

export default function Home(props) {
    return (
        <div>
            <Navbar />
            <Banner/>
            <Features />
            <HowItWorks />
            <Parameters />
            <Benefits />
            <Footer />
        </div>
    );
}