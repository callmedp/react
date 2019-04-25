import React, {Component} from 'react';
import './header.scss'
import {Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'
import {Link} from "react-router-dom";

export default class Header extends Component {

    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -63
        })
    }


    componentDidMount() {

        Events.scrollEvent.register('begin', function () {
            console.log("begin", arguments);
        });

        Events.scrollEvent.register('end', function () {
            console.log("end", arguments);
        });

    }

    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
    }

    render() {
        const {page} = this.props;
        return (
            <header className={this.props.getclass + " home-nav-fixed"}>
                <div className="container">
                    <Link to={'/resume-builder/'} className="container--logo"/>
                    {!!(page === 'home') &&
                    <ul className="home-links">
                        <li>
                            <a onClick={() => this.scrollTo('works')}>How it Works</a>
                        </li>
                        <li>
                            <a onClick={() => this.scrollTo('templates')}>Templates</a>
                        </li>
                    </ul>
                    }
                    <div className="signin">
                        {!!(page === 'home') &&
                        <button className="white-button mr-30" onClick={() => this.scrollTo('templates')}>Build your
                            resume
                        </button>
                        }
                        <span className="signin--user-pic">
            				<img src={`${this.staticUrl}react/assets/images/user-pic.jpg`}/>
            			</span>
                        Hello Amit
                    </div>
                </div>
            </header>
        )
    }

}