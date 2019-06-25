import React, {Component} from 'react';
import './header.scss'
import {connect} from "react-redux";
import {Events, scroller} from 'react-scroll'
import {Link} from "react-router-dom";
import {showHelpModal,hideHelpModal} from '../../../store/ui/actions/index';
import HelpModal from '../../Modal/helpModal';


class Header extends Component {

    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
    }

    scrollTo(elem,offset) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset
        })
    }


    componentDidMount() {

        Events.scrollEvent.register('begin', function () {
        });

        Events.scrollEvent.register('end', function () {
        });

    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }

    render() {
        const {page, userName, showHelpModal, ui:{helpModal}, hideHelpModal} = this.props;
        return (
            <header className={this.props.getclass + " home-nav-fixed"}>
             <HelpModal modalStatus={helpModal} hideHelpModal={hideHelpModal}/>
                <div className="container">
                    <Link to={'/resume-builder/'} className="container--logo"/>
                    {!!(page === 'home') &&
                    <ul className="home-links">
                        <li>
                            <a href="#work" onClick={() => this.scrollTo('works',-63)}>How it Works</a>
                        </li>
                        <li>
                            <a href='#template'onClick={() => this.scrollTo('templates',-50)}>Templates</a>
                        </li>
                    </ul>
                    }
                    <div className="signin">
                        <button className="white-button mr-15" onClick={() => {
                            showHelpModal()
                        }}>
                            Reach us
                        </button>
                        {!!(page === 'home') &&
                        <button className="white-button mr-30" onClick={() => this.scrollTo('templates',-60)}>Build your
                            resume
                        </button>
                        }
                        <span className="signin--user-pic">
            				<img alt="user info" src={`${this.staticUrl}react/assets/images/user-pic.jpg`}/>
            			</span>
                        Hello {userName || 'User'}
                    </div>
                </div>
            </header>
        )
    }

}
const mapStateToProps =(state) =>{
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

