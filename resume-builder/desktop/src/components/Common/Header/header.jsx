import React, {Component} from 'react';
import './header.scss'
import {connect} from "react-redux";
import {scroller} from 'react-scroll'
import {Link} from "react-router-dom";
import {showHelpModal, hideHelpModal} from '../../../store/ui/actions/index';
import HelpModal from '../../Modal/helpModal';


class Header extends Component {

    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.reachUsButton = this.reachUsButton.bind(this);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
    }

    scrollTo(elem,offset,action,label) {
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

    reachUsButton(){
        const {showHelpModal,eventClicked} =this.props;
        showHelpModal()
        eventClicked({
            'action':'ReachUs',
            'label':'Header'
        })
    }

    render() {
        const {page, userName, ui:{helpModal}, hideHelpModal,feedback,userInfo,eventClicked} = this.props;
        return (
            <header className={this.props.getclass + " home-nav-fixed"}>
             <HelpModal modalStatus={helpModal} hideHelpModal={hideHelpModal} userInfo={userInfo} feedback={feedback} eventClicked={eventClicked}/>
                <div className="container">
                    <Link to={'/resume-builder/'} className="container--logo"/>
                    {!!(page === 'home') &&
                    <ul className="home-links">
                        <li>
                            <span  onClick={() => this.scrollTo('works',-63,'Howitworks_Header','Header')}>How it Works</span>
                        </li>
                        <li>
                            <span onClick={() => this.scrollTo('templates',-50,'Templates','Header')}>Templates</span>
                        </li>
                    </ul>
                    }
                    <div className="signin">
                        {!!(page === 'home') &&
                        <React.Fragment>
                            <button className="white-button mr-15" onClick={this.reachUsButton}>
                                Reach us
                            </button>
                            <button className="white-button mr-30" onClick={()=>{this.scrollTo('templates',-60,'BuildResume','Header')}}>Build your
                                resume
                            </button>
                        </React.Fragment>
                        }
                        <span className="signin--user-pic">
            				<img alt="user info" src={`${this.staticUrl}react/assets/images/user-pic.jpg`}/>
            			</span>
                    </div>
                </div>
            </header>
        )
    }

}

const mapStateToProps = (state) => {
    return {
    ui: state.ui
    }
}

const mapDispatchToProps = (dispatch)=>{
    return {
        "showHelpModal": () =>{
            return dispatch(showHelpModal())
        },
        "hideHelpModal": ()=>{
            return dispatch(hideHelpModal())
        }
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(Header);

