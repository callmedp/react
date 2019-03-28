import React, {Component} from 'react';
import './header.scss'


export default class Header extends Component {
    render() {
        return (
            <header className="header">
            {/*
                <div className="header__left">
                    <button role="button" className="menu">
                        <i className="sprite icon--menu-bar"></i>
                    </button>
                </div>
            
                <a href="#" className="btn btn__round btn--outline">Back to home</a>
            */}

                <div className="header__left">
                    <button role="button" className="header__menu">
                        <i className="sprite icon--back-white"></i>
                    </button>

                    {/*<sapn>Resume Preview</sapn>*/}
                    <sapn>Choose your plan</sapn>
                </div>

                {/*<a href="#" className="btn btn__round btn--outline">Change template</a>*/}
            </header>
        )
    }

}