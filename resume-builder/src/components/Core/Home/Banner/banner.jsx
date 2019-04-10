import React, {Component} from 'react';
import './banner.scss'

export default class Banner extends Component {
    render() {
        return (
            <div className="banner-bg">
               <div className="banner-content">
                   <h1>Quickest Resume Builder</h1>
                   <p className="banner-content--txt">
                       <strong>Amit,</strong> secure the job you want with our resume builder
                   </p>
                   <ul>
                        <li><strong>10 years</strong> of expertise in resume building</li>
                        <li>Build your resume in a minute by importing your <strong>Shine profile</strong></li>
                        <li><strong>Download</strong> your customised resume anytime</li>
                        <li><strong>Highly customizable</strong> resume</li>
                        <li>Power to get you <strong>hired 33% faster</strong></li>
                   </ul>
                   <button className="orange-button banner-content--button">Build your resume</button>
               </div>
               <div className="banner-slider">
                    <img alt={"Banner"} src="/media/static/react/assets/images/home-banner-slider.png" className="img-responsive" />
               </div>
            </div>
        )
    }

}
