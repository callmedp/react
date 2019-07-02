import React, {Component} from 'react';
import './editPreview.scss'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx';
import RightSection from './RightSection/rightSection.jsx';
import Header from '../../Common/Header/header.jsx';
import * as actions from "../../../store/template/actions";
import {connect} from "react-redux";
import {withRouter} from "react-router-dom";
import * as profileActions from '../../../store/personalInfo/actions/index';
import * as uiActions from '../../../store/ui/actions/index';
import Loader from '../../Common/Loader/loader'
import {eventClicked} from '../../../store/googleAnalytics/actions/index'
import {formCategoryList} from '../../../Utils/formCategoryList'

class EditPreview extends Component {

    constructor(props){
        super(props);
        this.changeLink = this.changeLink.bind(this)
        this.headingChange = this.headingChange.bind(this);
    }

    componentDidMount() {
        this.props.fetchLoaderStatus()
        if(localStorage.getItem('personalInfo')){
            localStorage.setItem('newUser',true)
        }

    }

    changeLink(id,heading){
        this.props.headingChange(this.props.personalInfo,id,heading)
    }

    headingChange(entity,heading,pos){
        const {eventClicked,entityChange} = this.props
        eventClicked({
            'action':'EditSection',
            'label':formCategoryList[pos+1].name
        })
        entityChange(entity,heading,pos);
    }

    render() {
        const {history,ui:{mainloader}} = this.props;
        return (
            <div className="edit-section">
                {mainloader ? <Loader/> :""}
                {/* <NeedHelpModal/> */}
                <Header page={'edit'} history={history}/>
                <LeftSideBar {...this.props}/>
                <RightSection {...this.props} changeLink={this.changeLink} headingChange={this.headingChange}/>
            </div>

        )
    }
}
const mapStateToProps = (state) => {
    return {
        initialValues: state.template,
        template: state.template,
        personalInfo: state.personalInfo,
        ui:state.ui,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(actions.fetchTemplate())
        },
        "updateModalStatus": (data) => {
            return dispatch(actions.updateModalStatus(data))
        },
        'showGenerateResumeModal': () => {
            return dispatch(uiActions.showGenerateResumeModal())
        },
        'hideGenerateResumeModal': () => {
            return dispatch(uiActions.hideGenerateResumeModal())
        },
        "fetchPersonalInfo": () => {
            return dispatch(profileActions.fetchPersonalInfo())
        },
        'entityChange': (entity,heading,pos) => {
            entity[pos].entity_text = heading
            return new Promise((resolve, reject) => {
                return dispatch(profileActions.updateEntityPreference({"entity_preference_data": entity,resolve,reject}))
            })
        },
        "fetchLoaderStatus": () => {
            return dispatch(uiActions.fetchLoaderStatus())
        },
        "fetchAlertModalStatus": () => {
            return dispatch(uiActions.fetchAlertModalStatus())
        },
        "updateAlertModalStatus": (data) => {
            return dispatch(uiActions.updateAlertModalStatus(data))
        },
        'reGeneratePDF': (data) => {
            return dispatch(actions.reGeneratePDF(data))
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        }
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

