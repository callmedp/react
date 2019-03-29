import React, {Component} from 'react';
import {Link} from 'react-router-dom'
import './home.scss'
import * as actions from "../../../store/landingPage/actions";
import {connect} from "react-redux";

class Home extends Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.props.getCandidateId();
    }

    render() {
        return (
            <div>
                <Link to={'/resume-builder/edit/'}>Customize Your Resume</Link>
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
