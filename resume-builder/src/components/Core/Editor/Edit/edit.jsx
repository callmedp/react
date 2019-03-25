import React, {Component} from 'react';
import {withRouter, Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";

export default class Edit extends Component {
    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        const values = queryString.parse(this.props.location.search);

        this.state = {
            type: values && values.type || ''
        };
        if (!(values && values.type)) {
            console.log('here', this.props.history);
            this.props.history.push('/resume-builder/edit/?type=profile')
        }
    }


    handleSpanClick(e) {
        console.log('event ', e, this.context);
        e.stopPropagation();
        console.log('clickeddd');

    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: values && values.type || ''
            })
        }
    }

    render() {
        const {type} = this.state;
        return (
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                    <li className={type === 'profile' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=profile"> <span className="icon-info mr-20"></span>
                            Personal Info
                        </Link>
                    </li>
                    <li className={type === 'summary' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=summary">
                            <span className="icon-summary mr-20"></span>
                            Summary
                        </Link>
                        <span onClick={this.handleSpanClick} className="icon-delete pull-right">

                        </span>
                    </li>
                    <li className={type === 'experience' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=experience"><span className="icon-experience mr-20"></span>
                            Experience
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className={type === 'education' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=education">
                            <span className="icon-education mr-20"></span>
                            Education
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className={type === 'skill' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=skill">
                            <span className="icon-skills mr-20"></span>
                            Skills
                        </Link>
                        <span className="icon-delete pull-right"></span>
                    </li>
                    <li className="edit-section--addmore">
                        + Add more sections
                    </li>
                    <li className={type === 'language' ? 'edit-section--active' : ''}>
                        <Link to="/resume-builder/edit/?type=language">
                            <span className="icon-languages mr-20"></span>
                            Languages
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="">
                        <Link to="/resume-builder/edit/?type=award">
                            <span className="icon-awards mr-20"></span>
                            Awards
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="">
                        <Link to="/resume-builder/edit/?type=course">
                            <span className="icon-courses mr-20"></span>
                            Courses
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="">
                        <Link to="/resume-builder/edit/?type=project">
                            <span className="icon-projects mr-20"></span>
                            Projects
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>
                    <li className="">
                        <Link to="/resume-builder/edit/reference">
                            <span className="icon-references mr-20"></span>
                            References
                        </Link>
                        <span className="icon-add pull-right"></span>
                    </li>

                </ul>
            </div>
        )
    }

}