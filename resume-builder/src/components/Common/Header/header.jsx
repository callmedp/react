import React ,{Component} from 'react';
import './header.scss'
export default class Header extends Component {
    render(){
        return(
            <header>
            	<div className="container">
            		<a className="container--logo"></a>
            		<div className="signin">
            			<span className="signin--user-pic">
            				<img src="/images/user-pic.jpg" />
            			</span>
            			Hello Amit
            		</div>
            	</div>
            </header>
        )
    }

}