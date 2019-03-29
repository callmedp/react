import React, {Component} from 'react';
import {Link} from 'react-router-dom'
import './home.scss'
import * as actions from "../../../store/landingPage/actions";
import {connect} from "react-redux";
import Banner from "./Banner/banner.jsx";
import ResumeSlider from "./ResumeSlider/resumeSlider.jsx";
import Testimonial from "./Testimonial/testimonial.jsx";

class Home extends Component {
    constructor(props) {
        super(props);
        this.handleScroll = this.handleScroll.bind(this)
    }

    componentDidMount() {
        document.addEventListener('scroll', this.handleScroll);
        this.props.getCandidateId()
    }

    handleScroll() {

    }

    render() {
        return (
            <div>
                Hello
                <Link to={'/resume-builder/edit/'}>Customize Your Resume</Link>
                <Banner/>
                <ResumeSlider/>
                <Testimonial/>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
        "getCandidateId": () => {
            return dispatch(actions.getCandidateId())
        },

    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
