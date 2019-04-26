import React, {Component} from 'react';
import {connect} from "react-redux";
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

    renderSwitch() {
        const {entityList} = this.props;
        let entity;

        switch (this.state.type) {
            case 'profile': {
                return <PersonalInfo {...this.props}/>
            }

            case 'education': {
                entity = entityList && entityList[1];
                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Education {...this.props}/>
            }

            case 'experience': {
                entity = entityList && entityList[2];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Experience {...this.props}/>
            }

            case 'project': {
                entity = entityList && entityList[3];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Project {...this.props}/>
            }
            case 'skill': {
                entity = entityList && entityList[4];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Skill {...this.props}/>
            }
            case 'summary': {
                entity = entityList && entityList[5];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Summary {...this.props}/>
            }
            case 'award': {
                entity = entityList && entityList[6];
                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Award {...this.props}/>
            }
            case 'course': {
                entity = entityList && entityList[7];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Course {...this.props}/>
            }
            case 'language': {
                entity = entityList && entityList[8];

                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Language {...this.props}/>
            }
            case 'reference': {
                entity = entityList && entityList[9];
                return !!(!(entity && entity.active)) ? 
                <div className="backtoedit">
                    <p>Add more section in your resume from left panel</p>
                    <button className="orange-button">Back to Edit</button>
                </div>
                 : <Reference {...this.props}/>
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


const mapStateToProps = (state) => {
    return {
        entityList: state.personalInfo && state.personalInfo.entity_preference_data,
    }
}

export default connect(mapStateToProps, null)(RightSection)
