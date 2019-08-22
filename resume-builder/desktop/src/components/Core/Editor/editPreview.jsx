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
import {loginCandidate} from "../../../store/landingPage/actions"
import {
    customizeTemplate,
    fetchDefaultCustomization,
    reorderSection,
    reGeneratePDF
} from "../../../store/template/actions"
import * as profileActions from "../../../store/personalInfo/actions"
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
import queryString from "query-string";

class EditPreview extends Component {
    constructor(props) {
        super(props);
        this.removeNote = this.removeNote.bind(this);
        this.allowUploadResume = this.allowUploadResume.bind(this);
        this.state={
            visibleNote: true
        }
    }

    async componentDidMount() {
        const {analytics: {locationPath}, fetchEntityInfo, history: {location: {pathname}}, locationRouteChange, loginCandidate} = this.props
        if (!localStorage.getItem('candidateId')) {
            await loginCandidate()
        }
        fetchEntityInfo();
        if (localStorage.getItem('personalInfo')) {
            localStorage.setItem('newUser', true)
        }
    }

    removeNote() {
        localStorage.setItem('showNote', 'false')
        this.setState({
            visibleNote: false
        })
    }

    allowUploadResume() {
        let {userInfo: {upload_resume: uploadResume}, userInfo, updateSelectedTemplate} = this.props;
        userInfo['upload_resume'] = !uploadResume
        updateSelectedTemplate(userInfo)
    }

    render() {
        const {ui: {loader}, userInfo: {first_name, last_name, number, email, upload_resume: uploadResume}, history: {location: {pathname}}} = this.props;
        const showNote = localStorage.getItem('showNote') || '';
        const {visibleNote} = this.state;
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
                    {
                        pathname === '/resume-builder/preview/' && !!(!uploadResume) && !!(!showNote.length) && !!(visibleNote) &&
                        <div className="sticky-msg">
                        <span className="pt-20">
                            <figure>
                                <i className="icon-thumbsup"></i>
                                Well Done!
                            </figure>
                        </span>
                            <span>
                            <strong>Update Resume</strong>
                            <p>Your resume is ready to help you
                            search best jobs, update it on your
                            shine profile</p>
                            <button className="orange-button" onClick={this.allowUploadResume}>Update</button>
                        </span>
                            <i className="icon-close" onClick={this.removeNote}></i>
                        </div>
                    }
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
        },
        "loginCandidate": (token = '') => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({payload: {alt: ''}, resolve, reject, isTokenAvail: false}))
            })
        },
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

