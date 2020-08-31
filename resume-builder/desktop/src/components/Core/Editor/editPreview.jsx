import React, { Component } from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import { connect } from 'react-redux';
import RightSection from './RightSection/rightSection.jsx'
import { withRouter } from "react-router-dom";
import LoaderPage from "../../Loader/loaderPage.jsx";
import * as actions from "../../../store/ui/actions"
import { loginCandidate } from "../../../store/landingPage/actions"
import {
    customizeTemplate,
    fetchDefaultCustomization,
    reorderSection,
    reGeneratePDF
} from "../../../store/template/actions"
import { fetchPersonalInfo, updatePersonalInfo, getComponentTitle } from "../../../store/personalInfo/actions"
import SelectTemplateModal from '../../Modal/selectTemplateModal';
import {
    showAlertModal,
    hideAlertModal,
    previewButtonClicked,
    showGenerateResumeModal,
    hideGenerateResumeModal
} from '../../../store/ui/actions/index'
import moment from 'moment'
import { locationRouteChange, eventClicked } from '../../../store/googleAnalytics/actions/index'
import Swal from 'sweetalert2'
import { siteDomain } from '../../../Utils/domains'
import { storeTrackingInfo, updateProductAvailability, isTrackingInfoAvailable, getTrackingInfo } from '../../../Utils/common';
import { trackUser } from '../../../store/tracking/actions/index';

class EditPreview extends Component {
    constructor(props) {
        super(props);
        this.removeNote = this.removeNote.bind(this);
        this.allowUploadResume = this.allowUploadResume.bind(this);
        this.generateResumeAlert = this.generateResumeAlert.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
        this.state = {
            visibleNote: true
        }
    }

    sendTrackingInfo(action, pos) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId,
                triggerPoint, uId, position, utmCampaign } = getTrackingInfo();
            const {userTrack} = this.props;
            userTrack({ trackingId, productTrackingMappingId, productId, action, position,
                triggerPoint, uId, utmCampaign });
        }
    }

    async componentDidMount() {

        const queryString = new URLSearchParams(this.props.location.search);
        const trackingId = queryString.get('t_id')
        const triggerPoint = queryString.get('trigger_point')
        const uId = queryString.get('u_id')
        const position = queryString.get('position')
        const utmCampaign = queryString.get('utm_campaign')

        if(trackingId !== null){
            const productTrackingMappingId = '11'
            storeTrackingInfo(trackingId, productTrackingMappingId, '',
            triggerPoint,uId,position,utmCampaign)
        }
      
        // check if the userexperinece is greater or equal to 4 years. (7 is the pid for 4 years (mapping done here))

        if (parseInt(localStorage.getItem('userExperience') || 0) >= 7) {
            if (typeof document !== 'undefined' && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'none';
            }
        }
        else {
            if (typeof document !== 'undefined' && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'block';
            }
        }


        const { analytics: { locationPath }, fetchEntityInfo, history: { location: { pathname } }, locationRouteChange, loginCandidate } = this.props
        if (!localStorage.getItem('candidateId')) {
            await loginCandidate()
        }

        fetchEntityInfo();

        // get userInfo from LocalStorage
        if (localStorage.getItem('email')) window['email'] = localStorage.getItem('email')
        else window['email'] = ''
        if (localStorage.getItem('mobile')) window['mobile'] = localStorage.getItem('mobile')
        else window['mobile'] = ''
        if (localStorage.getItem('name')) window['name'] = localStorage.getItem('name')
        else window['name'] = ''


        if (localStorage.getItem('personalInfo')) {
            localStorage.setItem('newUser', true)
        }
    }

    static getActions() {
        return [getComponentTitle]
    }

    static async fetching({ dispatch }, params) {
        const actionList = EditPreview.getActions()
        const results = [];
        for (const [index, value] of actionList.entries()) {
            results[index] = await new Promise((resolve, reject) => dispatch(value({ info: params, resolve, reject })))
        }
        return results;
    }


    removeNote() {
        localStorage.setItem('showNote', 'false')
        this.setState({
            visibleNote: false
        })
    }

    allowUploadResume() {
        let { userInfo: { upload_resume: uploadResume }, userInfo, updateSelectedTemplate } = this.props;
        userInfo['upload_resume'] = !uploadResume
        updateSelectedTemplate(userInfo)
    }

    

    generateResumeAlert() {
        const { userInfo: { order_data, resume_generated }, previewButtonClicked, history, showGenerateResumeModal, reGeneratePDF, hideGenerateResumeModal } = this.props;
        if (order_data && order_data.id && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false)) {
            if (!resume_generated) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success blue-button ml-10',
                        cancelButton: 'btn btn-danger blue-button ml-10'
                    },
                    buttonsStyling: false
                })

                swalWithBootstrapButtons.fire({
                    title: 'Are you sure?',
                    text: "You won't be able to change your template again.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Yes, generate resume!',
                    cancelButtonText: 'No, cancel!',
                    reverseButtons: true
                }).then((result) => {
                    if (result.value) {
                        showGenerateResumeModal()
                        reGeneratePDF(order_data.id)
                        setTimeout(function () {
                            window.location.href = `${siteDomain}/dashboard`
                            hideGenerateResumeModal()
                        }, 5000);
                    }
                })
            }
            else {
                showGenerateResumeModal()
                reGeneratePDF(order_data.id)
                setTimeout(function () {
                    window.location.href = `${siteDomain}/dashboard`
                    hideGenerateResumeModal()
                }, 5000);
            }

        } else {
            history.push('/resume-builder/buy')
        }
    }

    render() {
        const { ui: { loader, alertModal, generateResumeModal }, reorderSection, fetchDefaultCustomization,
            customizeTemplate, previewButtonClicked, template: { entity_position, entity_id_count_mapping, heading_font_size, color, text_font_size },
            eventClicked, showSelectTemplateModal, showAlertModal,
            userInfo: { first_name, last_name, number, email, upload_resume: uploadResume, selected_template, order_data, resume_generated },
            history: { location: { pathname } } } = this.props;
        const showNote = localStorage.getItem('showNote') || '';
        const { visibleNote } = this.state;
        return (
            <div>
                {
                    !!(loader) &&
                    <LoaderPage />
                }
                <Header
                    userName={first_name}
                    lastName={last_name}
                    number={number}
                    email={email}
                    location={this.props.location}
                    
                />
                <div className="page-container">
                    <SelectTemplateModal
                        sendTrackingInfo={this.sendTrackingInfo}
                        {...this.props}
                        page={'edit'} />
                    <TopBar
                        eventClicked={eventClicked}
                        showSelectTemplateModal={showSelectTemplateModal}
                        userInfo={{ selected_template, order_data, resume_generated }}
                        showAlertModal={showAlertModal}
                    />
                    <section className={'flex-container mt-30'}>
                        <LeftSideBar
                            sendTrackingInfo = {this.sendTrackingInfo}
                            showAlertModal={showAlertModal}
                            eventClicked={eventClicked}
                            customizeTemplate={customizeTemplate}
                            fetchDefaultCustomization={fetchDefaultCustomization}
                            userInfo={{ selected_template }}
                            reorderSection={reorderSection}
                            template={{ entity_position, entity_id_count_mapping, heading_font_size, color, text_font_size }}
                            previewButtonClicked={previewButtonClicked}
                            onChange={this.allowUploadResume}
                            generateResumeAlert={this.generateResumeAlert}
                            ui={{ alertModal, generateResumeModal }}
                            match={this.props.match}
                        />

                        <RightSection
                            sendTrackingInfo = {this.sendTrackingInfo}
                            eventClicked={eventClicked}
                            generateResumeAlert={this.generateResumeAlert}
                        />
                    </section>
                    {
                        pathname === '/resume-builder/preview/' && !!(!uploadResume) && !!(!showNote.length) && !!(visibleNote) &&
                        < div className="sticky-msg">
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

                <Footer 
                sendTrackingInfo = {this.sendTrackingInfo}/>

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
                return dispatch(fetchPersonalInfo())
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
                return dispatch(fetchDefaultCustomization({ templateId, resolve, reject }))
            })
        },
        "updateSelectedTemplate": (personalDetails) => {
            const { gender, date_of_birth, extracurricular } = personalDetails;
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
                dispatch(updatePersonalInfo({ personalDetails, resolve, reject }));
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
                dispatch(loginCandidate({ info: { alt: '' }, resolve, reject, isTokenAvail: false }))
            })
        },
        "userTrack": (data) =>  {
            return  dispatch(trackUser(data))
          },
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

