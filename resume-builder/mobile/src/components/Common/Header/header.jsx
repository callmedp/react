import React, {Component} from 'react';
import './header.scss'
import {feedbackSubmit} from "../../../store/landingPage/actions";
import * as actions from "../../../store/sidenav/actions";
import {connect} from "react-redux";
import {Link} from 'react-router-dom';
import {showHelpModal, hideHelpModal} from "../../../store/ui/actions";
import NeedHelpModal from '../../Core/Home/NeedHelpModal/needHelpModal.jsx'


class Header extends Component {
    constructor(props) {
        super(props)
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }

    componentDidMount() {
        this.props.fetchSideNavStatus()
    }

    render() {
        const {
            page, history, updateModalStatus, backPage, order_data, showHelpModal, ui: {helpModal},
            userInfo: {first_name: userName, last_name: lastName, number, email}, submitFeedback, hideHelpModal
        } = this.props;

        return (
            <header className="header">
                <NeedHelpModal
                    modalStatus={helpModal}
                    firstName={userName}
                    lastName={lastName}
                    number={number}
                    email={email}
                    submitFeedback={submitFeedback}
                    hideHelpModal={hideHelpModal}
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
                    page === 'buy' ?
                        <React.Fragment>
                            <div className="header__left">
                                <button role="button" className="menu mr-10">
                                    <i className="sprite icon--back-white" onClick={() => {
                                        history.push('/resume-builder')
                                    }}></i>
                                </button>
                                <span>Choose your plan</span>
                            </div>

                            <div className="header__right">
                            <span className="header--off">
                                <img src={`${this.staticUrl}react/assets/images/mobile/50percentage-off.png`} alt=""/>
                            </span>
                            </div>

                        </React.Fragment>
                        :
                        page === 'preview' ?
                            <React.Fragment>
                                <div className="header__left">
                                    <button role="button" className="header__menu" onClick={() => {
                                        history.goBack()
                                    }}>
                                        <i className="sprite icon--back-white"></i>
                                    </button>

                                    {<span>Resume Preview</span>}
                                </div>
                                {order_data && order_data.id && !order_data.combo ? '' :
                                    <a className="btn btn__round btn--outline" onClick={() => {
                                        updateModalStatus({modal_status: true})
                                    }}>Change template</a>
                                }
                            </React.Fragment> :

                            page === 'menu' ?
                                <React.Fragment>
                                    <div className="header__left">
                                        <button role="button" className="header__menu"
                                                onClick={() => {
                                                    history.push(`/resume-builder/edit/?type=${backPage}}`)
                                                }}>
                                            <i className="sprite icon--back-white"></i>
                                        </button>

                                        {<span>Add / Remove</span>}
                                    </div>

                                </React.Fragment> :


                                <React.Fragment>
                                    <div className="header--logo">
                                        <img src={`${this.staticUrl}react/assets/images/mobile/logo.png`} alt=""/>
                                    </div>
                                    <div className="header--logo"></div>
                                    <a className="btn btn__transparent btn__round" onClick={showHelpModal}>Reach us</a>
                                </React.Fragment>}
            </header>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        ui: state.ui,
        userInfo: state.personalInfo,
        sidenav: state.sidenav
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
        'submitFeedback': (feedbackObj) => {
            return dispatch(feedbackSubmit(feedbackObj))
        },
        "showHelpModal": () => {
            return dispatch(showHelpModal())
        },
        "hideHelpModal": () => {
            return dispatch(hideHelpModal())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);