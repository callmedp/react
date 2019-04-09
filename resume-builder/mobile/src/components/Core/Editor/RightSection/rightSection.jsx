import React, {Component} from 'react';
import PersonalInfo from '../UserDetails/PersonalInfo/personalInfo.jsx';
import Summary from '../UserDetails/Summary/summary.jsx';
import Education from '../UserDetails/Education/education.jsx';
import Experience from '../UserDetails/Experience/experience.jsx';
import Skills from '../UserDetails/Skill/skill.jsx';
import Language from '../UserDetails/Language/language.jsx';
import Award from '../UserDetails/Award/award.jsx';
import Course from '../UserDetails/Course/course.jsx';
import Project from '../UserDetails/Project/project.jsx';
import Reference from '../UserDetails/Reference/references.jsx';
import './rightSection.scss'


export default class RightSection extends Component {

    render() {
        return (
            <div className="right-panel">
                <PersonalInfo/>
                {/*<Summary />*/}
                {/*<Education />*/}
                {/*<Experience />*/}
                {/*<Skills/>*/}
                {/*<Language/>*/}
                
            </div>
        )
    }

}