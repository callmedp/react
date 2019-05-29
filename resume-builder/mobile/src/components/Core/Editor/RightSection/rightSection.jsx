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
import {changeFormName} from "../../../../store/loader/actions/index";
import {connect} from "react-redux";
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
import Loader from '../../../Common/Loader/loader.jsx';

class RightSection extends Component {

    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)
        this.renderSwitch = this.renderSwitch.bind(this);
        this.state = {
            type: (values && values.type) || ''
        }
    }

    componentDidMount(){
        this.state.type === 'profile' ?
             this.props.changeFormName({formName:'personalInfo'}):
             this.props.changeFormName({formName:this.state.type})
    }


    componentDidUpdate(prevProps) {

        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search)
            this.setState({
                type: (values && values.type) || ''
            },()=>{     this.state.type === 'profile' ?
                        this.props.changeFormName({formName:'personalInfo'}): 
                        this.props.changeFormName({formName:this.state.type})
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
        const {info:{loader:{mainloader}}} = this.props
        return (
            <React.Fragment>
                {mainloader ? <Loader/>:''}
                <section id="right-panel-section" className="right-panel">
                    {
                        this.renderSwitch()
                    }
                </section>
            </React.Fragment>
        )
    }

}

const handleAddition = (fields,data,offset,type,containerId) =>{
    fields.push(data)

    scroller.scrollTo(`${type}${fields.length -1}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset,
        containerId
    })
}

const changeOrderingUp = (index,fields,event) => {
    
    event.stopPropagation();
    let currentItem = fields.get(index);
    let prevItem = fields.get(index - 1);
    currentItem['order'] = index - 1;
    prevItem['order'] = index;

    fields.splice(index -1 ,2,currentItem)
    fields.splice(index ,0,prevItem)
    return fields.getAll()
}

const changeOrderingDown = (index,fields,event) => {
    event.stopPropagation();
    let currentItem = fields.get(index);
    let nextItem = fields.get(index + 1);
    currentItem['order'] = index + 1;
    nextItem['order'] = index;

    fields.splice(index ,2,nextItem)
    fields.splice(index+1 ,0,currentItem)
    return fields.getAll()
}

const handleOrdering = (values) =>{
    values['list'].map((el,index)=>{
        el['order'] = index
    })
    return values
}

const previewHandling = async(callback,history) =>{
    await callback();
    history.push(`/resume-builder/preview`);
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        info: state,
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
        "changeFormName": (data) => {
            return dispatch(changeFormName(data))
        },
        "handleAddition":(fields,data,offset,type)=>{
            return handleAddition(fields,data,offset,type)
        },
        "handleOrdering":(values)=>{
            return handleOrdering(values)
        },
        "previewHandling":(callback,history)=>{
            return previewHandling(callback,history)
        },
        "changeOrderingUp":(index,fields,event)=>{
            return changeOrderingUp(index,fields,event)
        },
        "changeOrderingDown":(index,fields,event)=>{
            return changeOrderingDown(index,fields,event)
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(RightSection);