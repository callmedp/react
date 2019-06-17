import React, {Component} from 'react';
import './banner.scss'
import {Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'

export default class Banner extends Component {


    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'

    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -63
        })
    }

    componentDidMount() {
        Events.scrollEvent.register('begin', function () {
        });

        Events.scrollEvent.register('end', function () {
        });

    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }


    render() {
        const {userName} = this.props;
        return (

            <div className="banner-bg">
                <div className="banner-content">
                    <h1>Resume Builder <strong>by Experts</strong></h1>
                    <p className="banner-content--txt">
                        <strong>{userName || 'Hello'},</strong> secure the job you want with our resume builder
                    </p>
                    <ul>
                        <li> <span className="icon-builderexpert1"></span><strong>33% higher</strong> chances of shortlisting</li>
                        <li> <span className="icon-builderexpert2"></span><strong>10+ years</strong> of Resume Building Experience</li>
                        <li> <span className="icon-builderexpert3"></span>Resume data fetched from <strong>Shine profile</strong></li>
                    </ul>
                    <button className="orange-button banner-content--button"
                            onClick={() => this.scrollTo('templates')}>Build your resume
                    </button>
                </div>
                <div className="banner-slider">
                    <img alt={"Banner"}
                         src={`${this.staticUrlstaticUrl}react/assets/images/home-banner-slider.png`}
                         className="img-responsive"/>
                </div>
            </div>
        )
    }

}
