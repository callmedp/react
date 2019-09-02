import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import {connect} from 'react-redux';
import RightSection from './RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";
import LoaderPage from "../../Loader/loaderPage.jsx";
import * as actions from "../../../store/ui/actions"
import {
    customizeTemplate,
    fetchDefaultCustomization,
    reorderSection,
    reGeneratePDF
} from "../../../store/template/actions"
import {fetchPersonalInfo, updatePersonalInfo, getComponentTitle} from "../../../store/personalInfo/actions"
import SelectTemplateModal from '../../Modal/selectTemplateModal';
import {
    showAlertModal,
    hideAlertModal,
    previewButtonClicked,
    showGenerateResumeModal,
    hideGenerateResumeModal
} from '../../../store/ui/actions/index'
import moment from 'moment'
import {locationRouteChange, eventClicked} from '../../../store/googleAnalytics/actions/index'
import {loginCandidate} from "../../../store/landingPage/actions";

class EditPreview extends Component {

    componentDidMount() {
        const {analytics: {locationPath}, fetchEntityInfo, history: {location: {pathname}}, locationRouteChange} = this.props
        fetchEntityInfo();
        if (localStorage.getItem('personalInfo')) {
            localStorage.setItem('newUser', true)
        }
    }


    static getActions() {
        return [fetchPersonalInfo, getComponentTitle]
    }

    static async fetching({dispatch}, params) {
        const actionList = EditPreview.getActions()
        const results = [];
        for (const [index, value] of actionList.entries()) {
            results[index] = await new Promise((resolve, reject) => dispatch(value({info: params, resolve, reject})))
        }
        return results;
    }

    render() {
        const {ui: {loader}, userInfo: {first_name, last_name, number, email}} = this.props;
        return (
            <div>
                {
                    !!(loader) &&
                    <LoaderPage/>
                }
                <Header
                    userName={first_name}
                    lastName={last_name}
                    number={number}
                    email={email}/>
                <div className="page-container">
                    <SelectTemplateModal {...this.props} page={'edit'}/>
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
        template: state.template,
        analytics: state.analytics
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchEntityInfo": () => {
            return new Promise((resolve, reject) => {
                return dispatch(fetchPersonalInfo({info: '', resolve, reject}))
            })

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
                return dispatch(fetchDefaultCustomization({templateId, resolve, reject}))
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
                dispatch(updatePersonalInfo({personalDetails, resolve, reject}));
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
        },
        'previewButtonClicked': (data) => {
            return dispatch(previewButtonClicked(data))
        },
        'reGeneratePDF': (data) => {
            return dispatch(reGeneratePDF(data))
        },
        'showGenerateResumeModal': () => {
            return dispatch(showGenerateResumeModal())
        },
        'hideGenerateResumeModal': () => {
            return dispatch(hideGenerateResumeModal())
        },
        'locationRouteChange': (path) => {
            return dispatch(locationRouteChange(path))
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        }
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

