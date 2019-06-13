import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import {connect} from 'react-redux';
import RightSection from './RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";
import {siteDomain} from "../../../Utils/domains";
import LoaderPage from "../../Loader/loaderPage.jsx";
import * as actions from "../../../store/ui/actions"
import {customizeTemplate, fetchDefaultCustomization, reorderSection} from "../../../store/template/actions"
import * as profileActions from "../../../store/personalInfo/actions"
import SelectTemplateModal from '../../Modal/selectTemplateModal';
import {showAlertModal, hideAlertModal} from '../../../store/ui/actions/index'
import moment from 'moment'

class EditPreview extends Component {

    componentDidMount() {
        this.props.fetchEntityInfo();
        if(localStorage.getItem('personalInfo')){
            localStorage.setItem('newUser',true)
        }
    }


    render() {
        const {ui: {loader}, userInfo: {first_name}} = this.props;
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                {
                    !!(loader) &&
                    <LoaderPage/>
                }
                <Header userName={first_name}/>
                <div className="page-container">
                    <SelectTemplateModal {...this.props} page={'buy'}/>
                    <TopBar {...this.props}/>
                    <section className={'flex-container mt-30'}>
                        <LeftSideBar {...this.props}/>
                        <RightSection {...this.props}/>
                    </section>
                </div>
                <Footer/>

            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        ui: state.ui,
        userInfo: state.personalInfo,
        template: state.template
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchEntityInfo": () => {
            return dispatch(profileActions.fetchPersonalInfo())
        },
        "showSelectTemplateModal": () => {
            return dispatch(actions.showSelectTemplateModal())
        },
        "hideSelectTemplateModal": () => {
            return dispatch(actions.hideSelectTemplateModal())
        },

        "customizeTemplate": (data) => {
            return dispatch(customizeTemplate(data))
        },
        "fetchDefaultCustomization": (templateId) => {
            return new Promise((resolve, reject) => {
                return dispatch(fetchDefaultCustomization({templateId, resolve,reject}))
            })
        },
        "updateSelectedTemplate": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails;
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'gender': (gender && gender['value']) || '',
                    'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).map(el => el.value).join(',') : extracurricular
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "reorderSection": (payload) => {
            return dispatch(reorderSection(payload))
        },
        'showAlertModal': (alertType) => {
            return dispatch(showAlertModal(alertType))
        },
        'hideAlertModal': () => {
            return dispatch(hideAlertModal())
        }
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

