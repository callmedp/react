import React, {Component} from 'react';
import {withRouter, Link} from 'react-router-dom';
import './edit.scss'

export default class Edit extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.state = {
            code: 1
        }
        console.log('pro   ', props);
    }

    handleClick(clickId) {
        this.setState({
            code: clickId
        })
    }

    handleSpanClick(e) {
        console.log('event ', e, this.context);
        e.stopPropagation()
        console.log('clickeddd');

    }

    render() {
        const clickId = this.state.code;
        return (
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                    <li className={clickId === 1 ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=profile"> <span className="icon-info mr-10"></span>
                            Personal Info
                        </Link>
                    </li>
                    <li className={clickId === 2 ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=summary">
                            <span className="icon-summary mr-10"></span>
                            Summary
                        </Link>
                        <span onClick={this.handleSpanClick} className="icon-delete pull-right">

                        </span>
                    </li>
                    <li className={clickId === 3 ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=experience"><span className="icon-experience mr-10"></span>
                            Experience
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className={clickId === 4 ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=education">
                            <span className="icon-education mr-10"></span>
                            Education
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className={clickId === 5 ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=skill">
                            <span className="icon-skills mr-10"></span>
                            Skills
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className="edit-section--addmore">
                        + Add more sections
                    </li>
                    <li className="">
                        <Link to="/resume-builder/edit/?type=language">
                            <span className="icon-languages mr-10"></span>
                            Languages
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="hidden">
                        <Link to="/resume-builder/edit/?type=award">
                            <span className="icon-awards mr-10"></span>
                            Awards
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="hidden">
                        <Link to="/resume-builder/edit/?type=course">
                            <span className="icon-courses mr-10"></span>
                            Courses
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="hidden">
                        <Link to="/resume-builder/edit/?type=project">
                            <span className="icon-projects mr-10"></span>
                            Projects
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="hidden">
                        <Link to="/resume-builder/edit/reference">
                            <span className="icon-references mr-10"></span>
                            References
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>

                </ul>
            </div>
        )
    }

}