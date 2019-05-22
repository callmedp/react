import React, {Component} from 'react';
import './header.scss'
import * as actions from "../../../store/sidenav/actions";
import {connect} from "react-redux";
import {Link} from 'react-router-dom';


class Header extends Component {
    constructor(props) {
        super(props)
        this.openMenu = this.openMenu.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }

    openMenu() {
        this.props.updateSidenavStatus(true)
    }

    componentDidMount() {
        this.props.fetchSideNavStatus()
    }

    render() {
        const {page,history,updateModalStatus} = this.props;
        return (
            <header className="header">

                {page === 'edit' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="menu">
                                <i className="sprite icon--menu-bar" onClick={this.openMenu}></i>
                            </button>
                        </div>
                        <Link to={'/resume-builder'} className="btn btn__round btn--outline">Back to home</Link>
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
    
                        <a className="btn btn__round btn--outline" onClick={()=>{updateModalStatus({modal_status:true})}}>Change template</a>
                    </React.Fragment>:
                    <React.Fragment>
                        <div className="header--logo">
                            <img src={`${this.staticUrl}react/assets/images/mobile/logo.png`} alt=""/>
                        </div>
                        <div className="header--logo"></div>
                    </React.Fragment>}

                
                


            </header>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchSideNavStatus": () => {
            return dispatch(actions.fetchSideNavStatus())
        },
        "updateSidenavStatus": (status) => {
            ////console.log(status)
            return dispatch(actions.updateSidenavStatus(status))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);