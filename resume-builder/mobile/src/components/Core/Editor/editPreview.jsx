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
import {loginCandidate} from '../../../store/landingPage/actions/index';
import Loader from '../../Common/Loader/loader'
import {eventClicked} from '../../../store/googleAnalytics/actions/index'
import {formCategoryList} from '../../../Utils/formCategoryList'
import Swal from 'sweetalert2'
import { siteDomain } from '../../../Utils/domains';

class EditPreview extends Component {

    constructor(props) {
        super(props);
        if (parseInt(localStorage.getItem('experience') || 0) >= 4) {
            if(document.getElementsByClassName('chat-bot')){document.getElementsByClassName('chat-bot')[0].style.display = 'none';
            }
        }
        else {
            if(document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]){
                document.getElementsByClassName('chat-bot')[0].style.display = 'block';
            }
        }
        this.changeLink = this.changeLink.bind(this)
        this.headingChange = this.headingChange.bind(this);
        this.generateResumeAlert = this.generateResumeAlert.bind(this);
    }

    async componentDidMount() {
        if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
            await this.props.loginCandidate()
        }
        this.props.fetchPersonalInfo();
        this.props.fetchLoaderStatus()

         // get userInfo from LocalStorage
         if(localStorage.getItem('email')) window['email']= localStorage.getItem('email')
         else window['email']=''
         if(localStorage.getItem('mobile')) window['mobile'] = localStorage.getItem('mobile')
         else window['mobile']=''
         if(localStorage.getItem('name')) window['name'] = localStorage.getItem('name')
         else window['name']= ''
 

        if (localStorage.getItem('personalInfo')) {
            localStorage.setItem('newUser', true)
        }

    }

    changeLink(id, heading) {
        this.props.headingChange(this.props.personalInfo, id, heading)
    }

    headingChange(entity, heading, pos) {
        const {eventClicked, entityChange} = this.props
        eventClicked({
            'action': 'EditSection',
            'label': formCategoryList[pos + 1].name
        })
        entityChange(entity, heading, pos);
    }

    generateResumeAlert(){
        const { personalInfo: { order_data, resume_generated }, history, reGeneratePDF, showGenerateResumeModal, 
                hideGenerateResumeModal } = this.props;
        if (order_data && order_data.id) {
            if (!resume_generated) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success btn__round btn--outline',
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
        const {history, ui: {mainloader}} = this.props;
        return (
            <div className="edit-section">
                {mainloader ? <Loader/> : ""}
                <Header page={'edit'} history={history}/>
                <LeftSideBar {...this.props} generateResumeAlert={this.generateResumeAlert}/>
                <RightSection {...this.props} changeLink={this.changeLink} headingChange={this.headingChange}
                        generateResumeAlert={this.generateResumeAlert} />
            </div>

        )
    }
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
                dispatch(loginCandidate({payload: {alt: token}, resolve, reject, isTokenAvail: false}))
            })
        },
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

