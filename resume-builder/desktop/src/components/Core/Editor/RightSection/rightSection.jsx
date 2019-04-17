    import React, {Component} from 'react';
import './rightSection.scss'
import PersonalInfo from './UserDetails/PersonalInfo/personalInfo.jsx'
import Education from './UserDetails/Education/education.jsx'
import Experience from './UserDetails/Experience/experience.jsx'
import Language from './UserDetails/Language/language.jsx'
import Skill from './UserDetails/Skill/skill.jsx'
import Summary from './UserDetails/Summary/summary.jsx'
import Award from './UserDetails/Award/award.jsx'
import Project from './UserDetails/Project/project.jsx'
import Reference from './UserDetails/Reference/reference.jsx'
import Course from './UserDetails/Course/course.jsx'
import Template from './Template/template.jsx'
import queryString from 'query-string'


export default class RightSection extends Component {
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

    renderSwitch() {

        switch (this.state.type) {
            case 'profile': {
                return <PersonalInfo {...this.props}/>
            }

            case 'education': {
                return <Education {...this.props}/>
            }
            case 'skill': {
                return <Skill {...this.props}/>
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
                return <Template {...this.props} />
            }

        }

    }

    render() {
        const {type} = this.state;
        return (
            <section className="right-sidebar">
                {
                    this.renderSwitch()
                }
            </section>
        )
    }

}