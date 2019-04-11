import React, {Component} from 'react';
import './header.scss'


export default class Header extends Component {
    constructor(props){
        super(props)
    }
    render() {
        const {page} = this.props;
        return (
            <header className="header">
            
                { page === 'edit' ?
                    <React.Fragment>
                        <div className="header__left">
                            <button role="button" className="menu">
                                <i className="sprite icon--menu-bar"></i>
                            </button>
                        </div>
                        <a href="#" className="btn btn__round btn--outline">Back to home</a>
                    </React.Fragment>
                :   <React.Fragment>
                        <div className="header--logo">
                            <img src="/media/static/react/assets/images/mobile/logo.png" alt="" />
                        </div>
                        <div className="header--logo"></div>
                    </React.Fragment>}
            

                {/*<div className="header__left">
                    <button role="button" className="header__menu">
                        <i className="sprite icon--back-white"></i>
                    </button>

                    {<sapn>Resume Preview</sapn>}
                    <sapn>Choose your plan</sapn>
        </div>*/}

                {/*<a href="#" className="btn btn__round btn--outline">Change template</a>*/}
                
                

            </header>
        )
    }

}