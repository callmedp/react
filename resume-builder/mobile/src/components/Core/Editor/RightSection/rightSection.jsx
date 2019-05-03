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
import DataLoader from "../../../Common/DataLoader/dataloader"

class RightSection extends Component {

    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)
        this.renderSwitch = this.renderSwitch.bind(this);
        this.state = {
            type: (values && values.type) || ''
        }
        // this.educationRef = React.createRef()
        // this.skillRef = React.createRef()
    }


    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            // console.log('-pros----', queryString.parse(prevProps.location.search), prevProps);
            // let form_name =Object.keys(prevProps.info.form)[0]
            // console.log(form_name)
            // console.log("---- prev",)
            // let error = false
            // let list_values =prevProps.info.form[form_name]["syncErrors"]
            // if(list_values){
            //     for(let i of  list_values['list']){
            //         for(let j in Object.keys(i)){
            //             if(i[j]){
            //                 error =true
            //                 break;
            //             }
            //         }
            //     }
            // }
            
            // console.log("error",error)
            // if(!error){
            //     let form_values = prevProps.info.form[form_name]['values']
            //     form_name =form_name.toLowerCase()

            //     console.log("values",form_values)
            //     if(this.refs[form_name]){
            //         let prop = this.refs[form_name]
            //         console.log(prop)
            //         prop = prop['selectChildElement']('<Education/>')
            //         console.log(prop)
            //     }
            // }
            // console.log("info ------",prevProps.info)
            
            const values = queryString.parse(this.props.location.search)
            this.setState({
                type: (values && values.type) || ''
            })
        }
    }

    componentDidMount() {
        ////console.log(this.props)
        
    }

    renderSwitch() {
        switch (this.state.type) {
            case 'education': {
                return <Education ref={'education'} {...this.props}/>
            }
            case 'skill': {
                return <Skills ref={'skill'} {...this.props}/>
            }
            case 'experience': {
                return <Experience ref={'experience'} {...this.props}/>
            }
            case 'language': {
                return <Language ref={'language'} {...this.props}/>
            }
            case 'award': {
                return <Award ref={'award'} {...this.props}/>
            }
            case 'project': {
                return <Project ref={'project'} {...this.props}/>
            }
            case 'course': {
                return <Course ref={'course'} {...this.props}/>
            }
            case 'reference': {
                return <Reference ref={'reference'} {...this.props}/>
            }
            case 'summary': {
                return <Summary ref={'summary'} {...this.props}/>
            }
            default: {
                return <PersonalInfo ref={'profile'} {...this.props}/>
            }

        }

    }

    render() {
        const {type} = this.state;
        return (
            <React.Fragment>
                <section className="right-panel">
                    {
                        this.renderSwitch()
                    }
                </section>
            </React.Fragment>
        )
    }

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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(RightSection);