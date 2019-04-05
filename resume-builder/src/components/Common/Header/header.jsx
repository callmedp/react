import React ,{Component} from 'react';
import './header.scss'
export default class Header extends Component {
    redirectToEdit(){
        window.location.href = 'http://127.0.0.1:8000/resume-builder/edit/'
    }
    render(){
        return(
            <header className="home-nav-fixed">
            	<div className="container">
            		<a className="container--logo"></a>
                    <ul className="home-links">
                        <li>
                            <a href="#works">How it Works</a>
                        </li>
                        <li>
                            <a href="#templates">Templates</a>
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