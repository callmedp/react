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
        "headingChange": (personalInfo,id,heading) => {

            let { date_of_birth, extracurricular,image,gender} = personalInfo;
            let interest = extracurricular
            interest =  ((interest|| []).filter((item)=>item !==null).map((item)=>item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    entity_preference_data:(personalInfo.entity_preference_data).map((item,key)=>{
                        if(key === id){
                            item.entity_text = heading
                        }
                        return item
                    }),
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular': interest,
                    'image':image,
                    'gender':gender
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "fetchLoaderStatus": () => {
            return dispatch(uiActions.fetchLoaderStatus())
        },
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

