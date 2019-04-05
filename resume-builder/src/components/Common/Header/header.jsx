import React ,{Component} from 'react';
import './header.scss'
import { Link, DirectLink, Element, Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
export default class Header extends Component {
    
    constructor(props) {
        super(props);
        this.scrollTo = this.scrollTo.bind(this);
    }
    redirectToEdit(){
        window.location.href = '/resume-builder/edit/'
    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
          duration: 800,
          delay: 0,
          smooth: 'easeInOutQuad',
          offset:'100'
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
    
    render(){
        return(
            <header className="home-nav-fixed">
            	<div className="container">
            		<a className="container--logo"></a>
                    <ul className="home-links">
                        <li>
                            <a onClick={() => this.scrollTo('works')}>How it Works</a>
                        </li>
                        <li>
                            <a onClick={() => this.scrollTo('templates')}>Templates</a>
                        </li>
                    </ul>
            		<div className="signin">
                        <button className="white-button mr-30" onClick={this.redirectToEdit.bind(this)}>Build your resume</button>
            			<span className="signin--user-pic">
            				<img src="/media/static/react/assets/images/user-pic.jpg" />
            			</span>
            			Hello Amit
            		</div>
            	</div>
            </header>
        )
    }

}