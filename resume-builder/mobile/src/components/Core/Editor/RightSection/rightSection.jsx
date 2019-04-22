import React, {Component} from 'react';
import PersonalInfo from './UserDetails/PersonalInfo/personalInfo.jsx';
import Summary from './UserDetails/Summary/summary.jsx';
import Education from './UserDetails/Education/education.jsx';
import Experience from './UserDetails/Experience/experience.jsx';
import Skills from './UserDetails/Skill/skill.jsx';
import Language from './UserDetails/Language/language.jsx';
import Award from './UserDetails/Award/award.jsx';
import Course from './UserDetails/Course/course.jsx';
import Project from './UserDetails/Project/project.jsx';
import Reference from './UserDetails/Reference/references.jsx';
import './rightSection.scss'
import queryString from 'query-string'
import * as actions from "../../../../store/sidenav/actions";
import {connect} from "react-redux";


class RightSection extends Component {

    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)
        this.renderSwitch = this.renderSwitch.bind(this);
        this.state = {
            type: (values && values.type) || ''
        }
    }


    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search)
            this.setState({
                type: (values && values.type) || ''
            })
        }
    }

    componentDidMount() {
        this.props.fetchListOfLink()
    }

    renderSwitch() {

        switch (this.state.type) {
            case 'education': {
                return <Education {...this.props}/>
            }
            case 'skill': {
                return <Skills {...this.props}/>
            }
            case 'experience': {
                return <Experience {...this.props}/>
            }
            case 'language': {
                return <Language {...this.props}/>
            }
            case 'award': {
                return <Award {...this.props}/>
            }
            case 'project': {
                return <Project {...this.props}/>
            }
            case 'course': {
                return <Course {...this.props}/>
            }
            case 'reference': {
                return <Reference {...this.props}/>
            }
            case 'summary': {
                return <Summary {...this.props}/>
            }
            default: {
                return <PersonalInfo {...this.props}/>
            }

        }

    }

    render() {
        const {type} = this.state;
        return (
            <section className="right-panel">
                {
                    this.renderSwitch()
                }
            </section>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchListOfLink": () => {
            return dispatch(actions.fetchListOfLink())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(RightSection);