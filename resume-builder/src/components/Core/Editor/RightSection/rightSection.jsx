import React, {Component} from 'react';
import './rightSection.scss'
import PersonalInfo from '../UserDetails/PersonalInfo/personalInfo.jsx'
import Education from '../UserDetails/Education/education.jsx'
import Experience from '../UserDetails/Experience/experience.jsx'
import Language from '../UserDetails/Language/language.jsx'
import Skill from '../UserDetails/Skill/skill.jsx'
import Summary from '../UserDetails/Summary/summary.jsx'
import queryString from 'query-string'


export default class RightSection extends Component {
    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)

        this.state = {
            type: values  && values.type || ''
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search)
            this.setState({
                type: values && values.type || ''
            })
        }
    }

    render() {
        const {type} = this.state;
        return (
            <section className="right-sidebar">
                {
                    type === 'profile' ? <PersonalInfo/> :
                        type === 'education' ? <Education/> :
                            type === 'skill' ? <Skill/> :
                                type === 'experience' ? <Experience/> :
                                    type === 'summary' ? <Summary/> :
                                        type === 'language' ? <Language/> : ''
                }
            </section>
        )
    }

}