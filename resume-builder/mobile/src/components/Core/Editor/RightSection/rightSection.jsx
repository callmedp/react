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
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

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
        return (
            <React.Fragment>
                <section id="right-panel-section" className="right-panel">
                    {
                        this.renderSwitch()
                    }
                </section>
            </React.Fragment>
        )
    }

}

const handleAddition = (fields,data,offset,type) =>{
    fields.push(data)

    scroller.scrollTo(`${type}${fields.length -1}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset
    })
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        info: state
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchListOfLink": () => {
            return dispatch(actions.fetchListOfLink())
        },
        "updateCurrentLinkPos": (data) => {
            return dispatch(actions.updateCurrentLinkPos(data))
        },
        "handleAddition":(fields,data,offset,type)=>{
            return handleAddition(fields,data,offset,type)
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(RightSection);