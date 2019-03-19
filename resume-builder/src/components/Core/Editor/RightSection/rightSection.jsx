import React, {Component} from 'react';
import './rightSection.scss'
import PersonalInfo from '../UserDetails/PersonalInfo/personalInfo.jsx'

export default class RightSection extends Component {
    render() {
        return (
            <section className="right-sidebar">
                Right section
                <PersonalInfo/>
            </section>
        )
    }

}