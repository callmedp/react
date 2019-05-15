import React, {Component} from 'react';
import './home.scss'
import * as actions from "../../../store/landingPage/actions";
import {connect} from "react-redux";
import Banner from "./Banner/banner.jsx";
import ResumeSlider from "./ResumeSlider/resumeSlider.jsx";
import Testimonial from "./Testimonial/testimonial.jsx";
import Footer from "../../Common/Footer/footer.jsx";
import Header from "../../Common/Header/header.jsx";
import {Link} from 'react-router-dom'
import {Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll';
import queryString from "query-string";
import {hideModal, showModal} from "../../../store/ui/actions";
import {displaySelectedTemplate} from '../../../store/template/actions'


class Home extends Component {
    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.addclass = this.addclass.bind(this);
        this.state = {
            'scrolled': false,
            'token': ''
        }

        const values = queryString.parse(this.props.location.search);
        const token = (values && values.token) || '';
        this.state.token = token;
    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -10
        })
    }

    addclass() {
        let scrollpos = window.scrollY;
        if (scrollpos > 60) {
            this.setState({
                'scrolled': true
            })
        } else {
            this.setState({
                'scrolled': false
            })
        }
    }

    componentDidMount() {

        this.props.loginCandidate(this.state.token);
        Events.scrollEvent.register('begin', function () {
        });

        Events.scrollEvent.register('end', function () {
        });
        window.addEventListener('scroll', this.addclass);

    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }


    render() {
        const {userInfo: {first_name}} = this.props;
        return (
            <div className="nav-fixed">
                <Header page={'home'} userName={first_name} getclass={this.state.scrolled ? 'color-change' : ''}/>
                <Banner/>
                <section className="section-container">
                    <h2>Professional advantage</h2>
                    <strong className="section-container--sub-head">Resume builder advantages which will make your
                        career brighter</strong>
                    <ul className="advantages mt-30">
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage1"></span>
                            </div>
                            <div className="advantages--content">
                                <h3>A resume layout hat stands out </h3>
                                <p>Our resume layout optimizer makes sure all your content is aligned and organized so
                                    your resume looks like a work of art.</p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage2"></span>
                            </div>
                            <div className="advantages--content">
                                <h3>Create a great first impression to recruiters </h3>
                                <p>Our resume has the capability to catch recruiter’s attention fast as you just have 6
                                    secs to catch recruiter’s attention.</p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage3"></span>
                            </div>
                            <div className="advantages--content">
                                <h3>Increased recruiter views </h3>
                                <p>A creative, professional layout can grab a recruiter's attention. Each job has on an
                                    average of 500 applicants with 95% of resume never read. </p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage4"></span>
                            </div>
                            <div className="advantages--content">
                                <h3>Application Tracking Software (ATS) Friendly </h3>
                                <p>Most of the resume filtering is done by machine. So, it becomes very important to
                                    design your CV as per the ATS</p>
                            </div>
                        </li>
                    </ul>
                </section>

                <section id="works" className="section-container grey-bg">
                    <h2>How it works</h2>
                    <strong className="section-container--sub-head">Just 3 steps to create your perfect resume</strong>
                    <ul className="works mt-70">
                        <li className="works--list">
                            <div className="works--image">
                                <i>1</i>
                                <span className="icon-works1"></span>
                            </div>
                            <div className="works--content">
                                <h3>Choose your resume template</h3>
                                <p>Our professional resume templates are designed strictly following all industry
                                    guidelines and best practices employers are looking for.</p>
                            </div>
                        </li>
                        <li className="works--list">
                            <div className="works--image">
                                <i>2</i>
                                <span className="icon-works2"></span>
                            </div>
                            <div className="works--content">
                                <h3>Verify your profile imported from Shine</h3>
                                <p>We import your Shine Profile to create your resume automatically. You may edit the
                                    details, if required</p>
                            </div>
                        </li>
                        <li className="works--list">
                            <div className="works--image">
                                <i>3</i>
                                <span className="icon-works3"></span>
                            </div>
                            <div className="works--content">
                                <h3>Download your Resume</h3>
                                <p>Start impressing employers. Download your awesome resume and land the job you are
                                    looking for, effortlessly.</p>
                            </div>
                        </li>
                    </ul>
                </section>

                <ResumeSlider {...this.props}/>

                <section className="section-container">
                    <h2>Resume builder features</h2>
                    <strong className="section-container--sub-head">Customise the resume as per your needs</strong>
                    <ul className="features mt-30">
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features1"></span>
                            </div>
                            <div className="features--content">
                                <h3>Switch template</h3>
                                <p>Change the template any time you want while editing your resume</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features2"></span>
                            </div>
                            <div className="features--content">
                                <h3>Edit text</h3>
                                <p>You can edit the text on resume as well font size change</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features3"></span>
                            </div>
                            <div className="features--content">
                                <h3>Theme change</h3>
                                <p>We have different color theme which you can apply on your resume</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features4"></span>
                            </div>
                            <div className="features--content">
                                <h3>Move sections</h3>
                                <p>All sections on resume can be move anywhere where you want</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features5"></span>
                            </div>
                            <div className="features--content">
                                <h3>Upload image</h3>
                                <p>While editing you can upload your recent image on resume</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features6"></span>
                            </div>
                            <div className="features--content">
                                <h3>Preview resume</h3>
                                <p>At any stage of editing resume you can preview it</p>
                            </div>
                        </li>
                    </ul>

                    <button className="orange-button" onClick={() => this.scrollTo('templates')}>Build your resume
                    </button>

                </section>

                <Testimonial/>

                <Footer/>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        userInfo: state.personalInfo,
        ui: state.ui,
        template: state.template
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "getCandidateId": () => {
            return dispatch(actions.getCandidateId())
        },
        "loginCandidate": (token) => {
            return dispatch(actions.loginCandidate({alt: token}))
        },
        'showModal': () => {
            return dispatch(showModal())
        },
        'hideModal': () => {
            return dispatch(hideModal())
        },
        displaySelectedTemplate(templateId) {
            return dispatch(displaySelectedTemplate(templateId))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
