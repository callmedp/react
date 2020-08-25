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
import {changeFormName} from "../../../../store/ui/actions/index";
import {connect} from "react-redux";
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
import Loader from '../../../Common/Loader/loader.jsx';
import Swal from 'sweetalert2';
import propTypes from 'prop-types';


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
    const {info:{ui:{mainloader}}} = this.props
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

RightSection.propTypes = {
    changeFormName: propTypes.func,
    changeLink: propTypes.func,
    changeOrderingDown: propTypes.func,
    changeOrderingUp: propTypes.func,
    entityChange: propTypes.func,
    eventClicked: propTypes.func,
    fetchAlertModalStatus: propTypes.func,
    fetchListOfLink: propTypes.func,
    fetchLoaderStatus: propTypes.func,
    fetchPersonalInfo: propTypes.func,
    fetchTemplate: propTypes.func,
    generateResumeAlert: propTypes.func,
    getChatBot: propTypes.func,
    handleAddition: propTypes.func,
    handleOrdering: propTypes.func,
    headingChange: propTypes.func,
    hideGenerateResumeModal: propTypes.func,
    history: propTypes.shape({
        action: propTypes.string,
        block: propTypes.func,
        createHref: propTypes.func,
        go: propTypes.func,
        goBack: propTypes.func,
        goForward: propTypes.func,
        length: propTypes.number,
        listen: propTypes.func,
        location: propTypes.shape({
            hash: propTypes.string,
            pathname: propTypes.string,
            search: propTypes.string,
            state: undefined
        }),
        push: propTypes.func,
        replace: propTypes.func, 
    }),
    info: propTypes.object,
    initialValues: propTypes.shape({
        // currentLinkPos: propTypes.number,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
    loginCandidate: propTypes.func,
    match: propTypes.shape({
        isExact: propTypes.bool,
        params: propTypes.object,
        path: propTypes.string,
        url: propTypes.string,
    }),
    personalInfo: propTypes.shape({
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        gender: propTypes.string,
        hide_subscribe_button: propTypes.bool,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
    }),
    reGeneratePDF: propTypes.func,
    routes: propTypes.func,
    showGenerateResumeModal: propTypes.func,
    sidenav: propTypes.shape({
        // currentLinkPos: propTypes.number,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    staticContext: propTypes.func,
    template: propTypes.shape({
        color: propTypes.number,
        entity_position: propTypes.array,
        heading_font_size: propTypes.number,
        html: propTypes.string,
        modal_status: propTypes.bool,
        reorderFailToast: propTypes.bool,
        templateImage: propTypes.string,
        text_font_size: propTypes.number,
        thumbnailImages: propTypes.array,
        zoomInHtml: propTypes.string,
    }),
    showAlertMessage: propTypes.func,
    ui: propTypes.shape({
        alertModal: propTypes.bool,
        alertType: propTypes.string,
        formName: propTypes.string,
        generateResumeModal: propTypes.bool,
        helpModal: propTypes.bool,
        loader: propTypes.bool,
        loginModal: propTypes.bool,
        modal: propTypes.bool,
        previewClicked: propTypes.bool,
        select_template_modal: propTypes.bool,
        showMoreSection: propTypes.bool,
        successLogin: propTypes.bool,
        suggestionModal: propTypes.bool,
        suggestionType: propTypes.string,
        suggestions: propTypes.array,
    }),
    updateAlertModalStatus: propTypes.func,
    updateCurrentLinkPos: propTypes.func,
    updateModalStatus: propTypes.func,
}

const handleAddition = (fields,data,offset,type,eventClicked,entity_name) =>{
    fields.push(data)
    
    scroller.scrollTo(`${type}${fields.length -1}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset,
    })
    
    eventClicked({
        'action':'AddNew',
        'label':entity_name
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

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        info: state,
    }
};

const showAlertMessage = () =>{
    Swal.fire(
        'You Can\'t add more!',
        'Please Fill current list first',
        'error'
        )
    }
    
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
            "handleAddition":(fields,data,offset,type,eventClicked,entity_name)=>{
                return handleAddition(fields,data,offset,type,eventClicked,entity_name)
            },
            "handleOrdering":(values)=>{
                return handleOrdering(values)
            },
            "changeOrderingUp":(index,fields,event)=>{
                return changeOrderingUp(index,fields,event)
            },
            "changeOrderingDown":(index,fields,event)=>{
                return changeOrderingDown(index,fields,event)
            },
            "showAlertMessage":()=>{
                return showAlertMessage()
            }
        }
    };
    
    export default connect(mapStateToProps, mapDispatchToProps)(RightSection);