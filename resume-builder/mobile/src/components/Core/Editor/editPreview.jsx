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
import moment from 'moment'

class EditPreview extends Component {

    constructor(props){
        super(props);
        this.changeLink = this.changeLink.bind(this)
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

    render() {
        const {history,ui:{mainloader}} = this.props;
        return (
            <div className="edit-section">
                {mainloader ? <Loader/> :""}
                <Header page={'edit'} history={history}/>
                <LeftSideBar {...this.props}/>
                <RightSection {...this.props} changeLink={this.changeLink}/>
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
        "fetchPersonalInfo": () => {
            return dispatch(profileActions.fetchPersonalInfo())
        },
        'headingChange': (entity,heading,pos) => {
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
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

