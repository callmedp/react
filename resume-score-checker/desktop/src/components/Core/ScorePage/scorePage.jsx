import React from 'react';
import Navbar from '../Home/Navbar/navbar';
import Footer from '../../Common/Footer/footer';
import InnerBanner from './InnerBanner/innerBanner'
export default function ScorePage(){
    return (
        <div>
        <Navbar></Navbar>
        <InnerBanner></InnerBanner>
        <Footer></Footer>
        </div>
    );
}