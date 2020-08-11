import React, {Component, PureComponent} from 'react';
import './banner.scss'
import {scroller} from 'react-scroll'
import propTypes from 'prop-types';

export default class Banner extends PureComponent {

    static propTypes = {
        eventClicked: propTypes.func,
        userName: propTypes.string
    }

    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
    }

    scrollTo(elem,action,label) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -63
        })
        this.props.eventClicked({
            action,
            label
        })
    }


    render() {
        const {userName} = this.props;
        return (

            <div className="banner-bg">
                <div className="banner-content">
                    <h1>Resume Builder <strong>by Experts</strong></h1>
                    <p className="banner-content--txt">
                        <strong>Hello,</strong> secure the job you want with our resume builder
                    </p>
                    <ul>
                        <li> <span className="icon-builderexpert1"></span><strong>33% higher</strong> chances of shortlisting</li>
                        <li> <span className="icon-builderexpert2"></span><strong>10+ years</strong> of Resume Building Experience</li>
                        <li> <span className="icon-builderexpert3"></span>Resume data fetched from <strong>Shine profile</strong></li>
                        <li> <span className="icon-builderexpert4"></span>Use <strong>resume builder for 12 months</strong> to create unlimited resume</li>
                    </ul>
                    <button className="orange-button banner-content--button"
                            onClick={() => this.scrollTo('templates','BuildResume','TopButton')}>Build your resume
                    </button>
                </div>
                <div className="banner-slider">
                    <img alt={"Banner"}
                         src={`${this.staticUrl}react/assets/images/home-banner-slider.png`}
                         className="img-responsive"/>
                </div>
            </div>
        )
    }

}
