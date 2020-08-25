import React, {Component} from 'react';
import './banner.scss'
import {scroller} from 'react-scroll';

export default class Banner extends Component {


    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.handleBuildYourResumeClick = this.handleBuildYourResumeClick.bind(this);
    }

    scrollTo(elem, action, label) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -50
        })
        this.props.eventClicked({
            action,
            label
        })
    }

    handleBuildYourResumeClick(){
        this.scrollTo('templates', 'BuildResume', 'TopButton')
        this.props.sendTrackingInfo('home_page_build_your_resume',1);
    }

    render() {
        const {userName} = this.props;

        return (
            <section className="banner">
                <h1 className="mt-15">Resume Builder <br/> <strong>by Experts</strong></h1>
                <p><strong>Hello</strong>, secure the job you want with our
                    resume builder</p>

                <img src={`${this.staticUrl}react/assets/images/mobile/resume-bundel.png`} alt="Resume Templates"
                     className="img-fluid"/>
                <p className="text-center mt-5">
                    <a className="btn pt-10 pb-10 btn__round btn__primary btn__shadow" alt="Build Your Resume"
                       onClick={ this.handleBuildYourResumeClick}>Build your resume</a>
                </p>
                <ul className="resume-pointer">
                    <li>
                        <span className="sprite icon--shortlisting mr-5"></span>
                        <span><strong>33% higher</strong> chances of shortlisting</span>
                    </li>
                    <li>
                        <span className="sprite icon--experience-home mr-5"></span>
                        <span><strong>10+ years</strong> of Resume Building Experience</span>
                    </li>
                    <li>
                        <span className="sprite icon--profile mr-5"></span>
                        <span>Resume data fetched from <strong>Shine profile</strong></span>
                    </li>
                    <li>
                        <span className="sprite icon--create-download mr-5"></span>
                        <span>Use <strong>resume builder for 12 months</strong> to
                        create unlimited resume</span>
                    </li>
                </ul>
            </section>
        )
    }

}
