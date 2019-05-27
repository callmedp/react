import React, {Component} from 'react';
import './banner.scss'
import {Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'

export default class Banner extends Component {


    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -50
        })
    }

    componentDidMount() {


    }

    componentWillUnmount() {

    }


    render() {
        return (
            <section className="banner">
                <h1 className="mt-15">Resume Builder <br/> <strong>by Experts</strong></h1>
                <p><strong>Amit</strong>, secure the job you want with our
                    resume builder</p>

                <img src={`${this.staticUrl}react/assets/images/mobile/resume-bundel.png`} alt=""
                     className="img-fluid"/>
                <p className="text-center mt-5">
                    <a className="btn pt-10 pb-10 btn__round btn__primary" onClick={() => this.scrollTo('templates')}>Build
                        your resume</a>
                </p>
                <ul className="resume-pointer">
                    <li>
                        {/* <span className="sprite icon--higher"></span> */}
                        <span><strong>33% higher</strong> chances of shortlisting</span>
                    </li>
                    <li>
                        <span className="sprite icon-experience"></span>
                        <span><strong>10+ years</strong> of Resume Building Experience</span>
                    </li>
                    <li>
                        <span className="sprite icon-profile"></span>
                        <span>Resume data fetched from <strong>Shine profile</strong></span>
                    </li>
                </ul>
            </section>
        )
    }

}
