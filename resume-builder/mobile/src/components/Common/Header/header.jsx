import React, { Component } from 'react';
import './header.scss'
import { feedbackSubmit } from "../../../store/landingPage/actions";
import * as actions from "../../../store/sidenav/actions";
import { showHelpModal, hideHelpModal } from "../../../store/ui/actions/index"
import { connect } from "react-redux";
import NeedHelpModal from '../../Core/Home/NeedHelpModal/needHelpModal.jsx'


class Header extends Component {
    constructor(props) {
        super(props)
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.reachUsButton = this.reachUsButton.bind(this);
        this.changeTemplate = this.changeTemplate.bind(this);
    }

    componentDidMount() {
        this.props.fetchSideNavStatus()
    }

    reachUsButton() {
        const { showHelpModal, eventClicked } = this.props;
        showHelpModal()
        eventClicked({
            'action': 'ReachUs',
            'label': 'Header'
        })
    }

    changeTemplate() {
        const { updateModalStatus, eventClicked } = this.props;
        updateModalStatus({ modal_status: true });
        let eventData = {
            'action': 'ChangeTemplate',
            'label': 'ResumeCreation'
        }
        eventClicked(eventData);
    }

    render() {
        const {
            page, history, backPage, order_data, ui: { helpModal },
            personalInfo, personalInfo: { resume_generated }, feedback, hideHelpModal, eventClicked
        } = this.props;

        return (
            <header className="header">
                <NeedHelpModal
                    modalStatus={helpModal}
                    personalInfo={personalInfo}
                    feedback={feedback}
                    hideHelpModal={hideHelpModal}
                    eventClicked={eventClicked}
                />
                {page === 'edit' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="menu mr-10">
                                <i className="sprite icon--back-white" onClick={() => {
                                    history.push('/resume-builder')
                                }}></i>
                            </button>
                            <span>Customise your resume</span>
                        </div>

                    </React.Fragment>
                    :
                    page === 'preview' ?
                        <React.Fragment>
                            <div className="header__left">
                                <button role="button" className="header__menu" onClick={() => { history.goBack() }}>
                                    <i className="sprite icon--back-white"></i>
                                </button>

                                {<span>Resume Preview</span>}
                            </div>
                            {
                                (order_data && order_data.id && order_data.combo) ? <a className="btn btn__round btn--outline" alt="Change Template" onClick={this.changeTemplate}>Change template</a>
                                    : (order_data && order_data.id && order_data.expiry &&  localStorage.getItem('subscriptionActive')) ? <a className="btn btn__round btn--outline" alt="Change Template" onClick={this.changeTemplate}>Change template</a> :
                                        (!(order_data && order_data.id) || !(resume_generated)) ?
                                            <a className="btn btn__round btn--outline" alt="Change Template" onClick={this.changeTemplate}>Change template</a> : ''
                            }
                        </React.Fragment> :
                        page === 'buy' ?
                            <React.Fragment>
                                <div className="header__left">
                                    <button role="button" className="menu mr-10">
                                        <i className="sprite icon--back-white" onClick={() => {
                                            // history.push('/resume-builder/edit')
                                            history.goBack()
                                        }}></i>
                                    </button>
                                    <span>Choose your plan</span>
                                </div>

                                {/* <div className="header__right"></div> */}

                            </React.Fragment> :

                            page === 'menu' ?
                                <React.Fragment>
                                    <div className="header__left">
                                        <button role="button" className="header__menu"
                                            onClick={() => { history.push(`/resume-builder/edit/?type=${backPage}`) }}>
                                            <i className="sprite icon--back-white"></i>
                                        </button>

                                        {<span>Add / Remove</span>}
                                    </div>

                                </React.Fragment> :

                                <React.Fragment>
                                    <div className="header--logo">
                                        <img src={`${this.staticUrl}react/assets/images/mobile/logo.png`} alt="Logo" />
                                    </div>
                                    <div className="header--logo"></div>
                                    <a className="btn btn__transparent btn__round" alt="Reach Us" onClick={this.reachUsButton}>Reach us</a>
                                </React.Fragment>}
            </header>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        ui: state.ui,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchSideNavStatus": () => {
            return dispatch(actions.fetchSideNavStatus())
        },
        "updateSidenavStatus": (status) => {
            return dispatch(actions.updateSidenavStatus(status))
        },
        "showHelpModal": () => {
            return dispatch(showHelpModal())
        },
        "hideHelpModal": () => {
            return dispatch(hideHelpModal())
        },
        'feedback': (values) => {
            return dispatch(feedbackSubmit(values))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);