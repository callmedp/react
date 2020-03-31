import React, { Component } from "react";


class Features extends Component {
    render(){
        return (
            <div className="features pb-15">
                <ul className="features__lists">
                    <li className="features__item">
                        <i className="sprite layout-resume"></i>
                        <p className="mb-0 mt-3 font-weight-bold text-center">Better formatting <br/>&amp; layout of Resume </p>
                    </li>
    
                    <li className="features__item">
                        <i className="sprite tips"></i>
                        <p className="mb-0 mt-3 font-weight-bold text-center">Tips to improve the resume to stand you out</p>
                    </li>
                    
                    <li className="features__item">
                        <i className="sprite review-score"></i>
                        <p className="mb-0 mt-3 font-weight-bold text-center">Detailed review of each section with score</p>
                    </li>
                    
                    <li className="features__item">
                        <i className="sprite expert-guidance"></i>
                        <p className="mb-0 mt-3 font-weight-bold text-center">Expert Guidance to increase resume views</p>
                    </li>
                </ul>
            </div>
        );
    }
}

export default Features;