import React, {Component} from 'react';
import './resumeSlider.scss'

export default class ResumeSlider extends Component {
    constructor(props) {
        super(props)
    }


    render() {
        return (
            <section id="templates" className="section-container">
                <h2>Proven resume templates</h2>
                <strong className="section-container--sub-head">Choose from a library of classic templates and land a new job</strong>
                <ul className="slider">
                    <li><img src="/images/slider.jpg" className="img-responsive" /></li>
                </ul>
            </section>
        )
    }

}
