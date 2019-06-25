import React, {Component} from 'react';
import './header.scss'
import * as actions from "../../../store/sidenav/actions";
import {showHelpModal,hideHelpModal} from "../../../store/ui/actions/index"
import {feedbackSubmit} from "../../../store/landingPage/actions/index"
import {connect} from "react-redux";
import {Link} from 'react-router-dom';
import NeedHelpModal from '../../Core/Home/NeedHelpModal/needHelpModal';


class Header extends Component {
    constructor(props) {
        super(props)
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }

    componentDidMount() {
        this.props.fetchSideNavStatus()
    }

    render() {
        const {page,history,updateModalStatus,backPage,order_data,ui:{helpModal},showHelpModal,hideHelpModal,personalInfo,feedback} = this.props;
        return (
            <header className="header">
                <NeedHelpModal modalStatus={helpModal} personalInfo={personalInfo} hideHelpModal={hideHelpModal} feedback={feedback}/>
                {page === 'edit' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="menu mr-10">
                                <i className="sprite icon--back-white" onClick={()=>{history.push('/resume-builder')}}></i>
                            </button>
                            <span>Customise your resume</span>
                        </div>
                        
                    </React.Fragment>
                    : 
                    page === 'preview' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="header__menu" onClick={()=>{history.goBack()}}>
                                <i className="sprite icon--back-white"></i>
                            </button>
    
                            {<span>Resume Preview</span>}
                        </div>
                        {order_data && order_data.id && !order_data.combo ? '':
                            <a className="btn btn__round btn--outline" onClick={()=>{updateModalStatus({modal_status:true})}}>Change template</a>
                        }
                    </React.Fragment>:
                    
                    page === 'menu' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="header__menu" 
                                onClick={()=>{history.push(`/resume-builder/edit/?type=${backPage}}`)}}>
                                <i className="sprite icon--back-white"></i>
                            </button>
    
                            {<span>Add / Remove</span>}
                        </div>
    
                    </React.Fragment>:


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
        "showHelpModal": () =>{
            return dispatch(showHelpModal())
        },
        "hideHelpModal": ()=>{
            return dispatch(hideHelpModal())
        },
        'feedback': (values) => {
            return dispatch(feedbackSubmit(values))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);