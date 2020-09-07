import React, { Component } from 'react';
import './header.scss'
import { connect } from "react-redux";
import { scroller } from 'react-scroll'
import { Link } from "react-router-dom";
import { showHelpModal, hideHelpModal } from '../../../store/ui/actions/index';
import HelpModal from '../../Modal/helpModal';
import queryString from "query-string";
import propTypes from 'prop-types';

class Header extends Component {
    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.reachUsButton = this.reachUsButton.bind(this);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.handleBuildYourResumeClick = this.handleBuildYourResumeClick.bind(this)
        this.handleTemplateClick = this.handleTemplateClick.bind(this)
        this.howItWorks = this.howItWorks.bind(this)
    }
    
    scrollTo(elem, offset, action, label) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset
        })
        
        this.props.eventClicked({
            action,
            label
        })
    }
    
    reachUsButton() {
        const { showHelpModal, eventClicked } = this.props;
        this.props.sendTrackingInfo("header_reach_us",1)
        showHelpModal()
        eventClicked({
            'action': 'ReachUs',
            'label': 'Header'
        })
    }

    howItWorks(){
        this.scrollTo('works', -63, 'Howitworks_Header', 'Header')
        this.props.sendTrackingInfo('header_how_it_works',1)
    }

    handleTemplateClick(){
        this.scrollTo('templates', -50, 'Templates', 'Header')
        this.props.sendTrackingInfo('header_templates',1)
    }

    handleBuildYourResumeClick(){
         this.scrollTo('templates', -60, 'BuildResume', 'Header') 
         this.props.sendTrackingInfo('header_build_your_resume',1)
    }

    componentDidMount() {
        const values = queryString.parse(this.props.location.search);
        const template = (values && values.template) || '';
        
        if (template === "false") {
            this.scrollTo('templates', -50, 'Templates', 'Header')
        }
        
    }
    render() {
        const { page, userName,lastName, number,email, ui: { helpModal }, hideHelpModal, feedback, eventClicked } = this.props;
        return (
            <header className={this.props.getclass + " home-nav-fixed"}>
                <HelpModal modalStatus={helpModal} hideHelpModal={hideHelpModal} userInfo={{ userName, email, number }} feedback={feedback} eventClicked={eventClicked} />
                <div className="container">
                    <Link to={'/resume-builder/'} className="container--logo" />
                    {!!(page === 'home') &&
                        <ul className="home-links">
                            <li>
                                <span onClick={this.howItWorks}>How it Works</span>
                            </li>
                            <li>
                                <span onClick={this.handleTemplateClick}>Templates</span>
                            </li>
                        </ul>
                    }
                    <div className="signin">
                        {!!(page === 'home') &&
                            <React.Fragment>
                                {
                                    !!(localStorage.getItem('candidateId')) &&
                                    <button className="white-button mr-15" onClick={this.reachUsButton}>
                                        Reach us
                                </button>
                                }
                                <button className="white-button mr-30" onClick={this.handleBuildYourResumeClick}>Build your
                                        resume
                            </button>
                            </React.Fragment>
                        }
                        {!!(page !== 'home') &&
                            <React.Fragment>
                                <span className="signin--user-pic">
                                    <img alt="user info" src={`${this.staticUrl}react/assets/images/user-pic.jpg`} />
                                </span>
                                <span>
                                    Hello {userName || 'User'}
                                </span>
                            </React.Fragment>
                        }
                    </div>
                </div>
            </header>
    
)
}

}

Header.propTypes = {
    email: propTypes.string,
    eventClicked: propTypes.func,
    feedback: propTypes.func,
    getclass: propTypes.string,
    hideHelpModal: propTypes.func,
    number: propTypes.string,
    page: propTypes.string,
    showHelpModal: propTypes.func,
    userName: propTypes.string,
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
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
}

const mapStateToProps = (state) => {
    return {
        ui: state.ui
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "showHelpModal": () => {
            return dispatch(showHelpModal())
        },
        "hideHelpModal": () => {
            return dispatch(hideHelpModal())
        }
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Header);

