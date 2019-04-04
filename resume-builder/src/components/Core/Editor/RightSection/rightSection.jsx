import React, {Component} from 'react';
import PersonalInfo from '../UserDetails/PersonalInfo/personalInfo';
import Summary from '../UserDetails/Summary/summary';
import Education from '../UserDetails/Education/education';
import Experience from '../UserDetails/Experience/experience';
import Skills from '../UserDetails/Skill/skill';
import Language from '../UserDetails/Language/language';
import Award from '../UserDetails/Award/award';
import Course from '../UserDetails/Course/course';
import Project from '../UserDetails/Project/project';
import Reference from '../UserDetails/Reference/references';
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