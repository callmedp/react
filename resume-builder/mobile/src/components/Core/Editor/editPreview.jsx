import React, {Component} from 'react';
import './editPreview.scss'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx';
import RightSection from './RightSection/rightSection.jsx';
import Header from '../../Common/Header/header.jsx';
import * as actions from "../../../store/template/actions";
import {connect} from "react-redux";
import {withRouter} from "react-router-dom";
import * as profileActions from '../../../store/personalInfo/actions/index';

class EditPreview extends Component {

    constructor(props){
        super(props);
        this.changeLink = this.changeLink.bind(this)
    }

    componentDidMount() {
        this.props.fetchTemplate()
    }

    changeLink(id,heading){
        this.props.headingChange(this.props.personalInfo,id,heading)
    }

    render() {
        return (
            <div className="edit-section">
                <Header page={'edit'}/>
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
        personalInfo: state.personalInfo
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
        "headingChange": (personalInfo,id,heading) => {
            console.log(personalInfo.entity_preference_data)
            let personalDetails = {
                ...personalInfo,
                ...{
                    entity_preference_data:(personalInfo.entity_preference_data).map((item,key)=>{
                        if(key === id){
                            item.entity_text = heading
                        }
                        return item
                    })
                ,
                    'extracurricular': ''
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

