import React from 'react';
import './features.scss'

const Features=props=>{
    return (

<section className="howItWork">
<div className="container h-100">
    <div className="row h-100 howItWork__wrap">
        <div className="col-md-3 h-100">
            <div className="d-flex flex-column align-items-center">
                <i className="sprite layout-resume"></i>
                <p className="mb-0 mt-3 font-weight-bold text-center">Better formatting <br/>&amp; layout of Resume</p>
            </div>
        </div>
        <div className="col-md-3 h-100">
            <div className="d-flex flex-column align-items-center">
                <i className="sprite tips"></i>
                <p className="mb-0 mt-3 font-weight-bold text-center">Tips to improve the <br/>resume to stand you out</p>
            </div>
        </div>
        <div className="col-md-3 h-100">
            <div className="d-flex flex-column align-items-center">
                <i className="sprite review-score"></i>
                <p className="mb-0 mt-3 font-weight-bold text-center">Detailed review of <br/>each section with score</p>
            </div>
        </div>
        <div className="col-md-3 h-100">
            <div className="d-flex flex-column align-items-center">
                <i className="sprite expert-guidance"></i>
                <p className="mb-0 mt-3 font-weight-bold text-center">Expert Guidance to <br/>increase resume views</p>
            </div>
        </div>
    </div>
</div>
</section>
    );
}

export default Features;