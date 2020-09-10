import React, { Component } from 'react';
import './editPreview.scss'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx';
import RightSection from './RightSection/rightSection.jsx';
import Header from '../../Common/Header/header.jsx';
import * as actions from "../../../store/template/actions";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import * as profileActions from '../../../store/personalInfo/actions/index';
import * as uiActions from '../../../store/ui/actions/index';
import { loginCandidate } from '../../../store/landingPage/actions/index';
import Loader from '../../Common/Loader/loader'
import { eventClicked } from '../../../store/googleAnalytics/actions/index'
import { formCategoryList } from '../../../Utils/formCategoryList'
import Swal from 'sweetalert2'
import { siteDomain } from '../../../Utils/domains';
import { trackUser } from '../../../store/tracking/actions/index';
import { isTrackingInfoAvailable, getTrackingInfo, storeTrackingInfo, updateProductAvailability } from '../../../Utils/common';
import {Helmet} from "react-helmet";
// import * as lscache from '../../../../node_modules/lscache/lscache';
import propTypes from 'prop-types';

class EditPreview extends Component {
    constructor(props) {
        super(props);
        this.changeLink = this.changeLink.bind(this)
        this.headingChange = this.headingChange.bind(this);
        this.generateResumeAlert = this.generateResumeAlert.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
    }

    sendTrackingInfo(action, pos) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId,
                triggerPoint, uId,  utmCampaign } = getTrackingInfo();
            const { userTrack } = this.props;
            let { position } = getTrackingInfo() 
            if(position === ""){
                position = pos;
            }
            userTrack({
                trackingId, productTrackingMappingId, productId, action, position,
                triggerPoint, uId, utmCampaign
            });
        }
    }

    async componentDidMount() {

        const queryString = new URLSearchParams(this.props.location.search);
        const trackingId = queryString.get('t_id') || ''
        const triggerPoint = queryString.get('trigger_point') || ''
        const uId = queryString.get('u_id') || localStorage.getItem("candidateId") || ''
        const position = queryString.get('position') || ''
        const utmCampaign = queryString.get('utm_campaign') || ''

        if (!!trackingId) {
            const productTrackingMappingId = '11'
            storeTrackingInfo(trackingId, productTrackingMappingId, '',
                triggerPoint, uId, position, utmCampaign)
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

        if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
            await this.props.loginCandidate()
        }
        this.props.fetchPersonalInfo();
        this.props.fetchLoaderStatus();
        await this.props.getChatBot();


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

    changeLink(id, heading) {
        this.props.headingChange(this.props.personalInfo, id, heading)
    }

    headingChange(entity, heading, pos) {
        const { eventClicked, entityChange } = this.props
        eventClicked({
            'action': 'EditSection',
            'label': formCategoryList[pos + 1].name
        })
        entityChange(entity, heading, pos);
    }

    generateResumeAlert() {
        const { personalInfo: { order_data, resume_generated }, history, reGeneratePDF, showGenerateResumeModal,
            hideGenerateResumeModal } = this.props;
        if (order_data && order_data.id && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false)) {
            if (!resume_generated) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success btn__round btn--outline mt-10',
                        cancelButton: 'btn btn-danger btn__round btn--outline mt-10'
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
        }
        else {
            history.push(`/resume-builder/buy`)
        }
    }

    render() {
        const { history, ui: { mainloader } } = this.props;
        return (
            <div className="edit-section">
                <Helmet
                    script={[
                        { "src": (localStorage.getItem('script_link') ? localStorage.getItem('script_link') : null), "type": "text/javascript" }
                    ]}
                />
                {mainloader ? <Loader /> : ""}
                <Header page={'edit'} history={history} />
                <LeftSideBar
                    {...this.props}
                    generateResumeAlert={this.generateResumeAlert}
                    sendTrackingInfo={this.sendTrackingInfo} />
                <RightSection {...this.props} changeLink={this.changeLink}
                    headingChange={this.headingChange}
                    generateResumeAlert={this.generateResumeAlert}
                    sendTrackingInfo={this.sendTrackingInfo} />
            </div>

        )
    }
}

EditPreview.propTypes = {
    entityChange: propTypes.func,
    eventClicked: propTypes.func,
    fetchAlertModalStatus: propTypes.func,
    fetchLoaderStatus: propTypes.func,
    fetchPersonalInfo: propTypes.func,
    fetchTemplate: propTypes.func,
    getChatBot: propTypes.func,
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
    initialValues: propTypes.shape({
        currentLinkPos: propTypes.string,
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
        currentLinkPos: propTypes.string,
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
    updateModalStatus: propTypes.func,
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.template,
        template: state.template,
        personalInfo: state.personalInfo,
        ui: state.ui,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(actions.fetchTemplate())
        },
        "getChatBot": () => {
            return new Promise((resolve, reject) => {
                return dispatch(profileActions.getChatBotUrl())
            })
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
        'entityChange': (entity, heading, pos) => {
            entity[pos].entity_text = heading
            return new Promise((resolve, reject) => {
                return dispatch(profileActions.updateEntityPreference({
                    "entity_preference_data": entity,
                    resolve,
                    reject
                }))
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
        },
        "loginCandidate": (token) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({ info: { alt: token }, resolve, reject, isTokenAvail: false }))
            })
        },
        "userTrack": (data) => dispatch(trackUser(data)),
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

