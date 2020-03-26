import React from 'react';
import Navbar from '../../Common/Navbar/navbar';
import Footer from '../../Common/Footer/footer';
import InnerBanner from './InnerBanner/innerBanner'
import ImproveScore from './ImproveScore/improveScore';
import ResumeReview from './ResumeReview/resumeReview';

export default function ScorePage() {
    return (
        <div>
            <Navbar />
            <InnerBanner />
            <ResumeReview />
            <ImproveScore />
            <Footer />
        </div>
    );
}