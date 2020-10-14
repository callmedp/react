import React from 'react';
import Navbar from '../../Common/Navbar/navbar';
import Footer from '../../Common/Footer/footer';
import InnerBanner from './InnerBanner/innerBanner'
import ImproveScore from './ImproveScore/improveScore';
import ResumeReview from './ResumeReview/resumeReview';
import GetExperts from './GetExperts/getExperts';

export default function ScorePage() {
    return (
        <div>
            <Navbar></Navbar>
            <InnerBanner></InnerBanner>
            <ResumeReview></ResumeReview>
            <ImproveScore></ImproveScore>
            <GetExperts></GetExperts>
            <Footer></Footer>
        </div>
    );
}