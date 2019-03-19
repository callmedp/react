import React ,{Component} from 'react';
import './edit.scss'
export default class Edit extends Component {
    render(){
        return(
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                	<li className="edit-section--active">
                		<span className="icon-info mr-10"></span>
                		Personal Info 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-summary mr-10"></span>
                		Summary 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-summary mr-10"></span>
                		Experience 
                		<span className="icon-experience pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-summary mr-10"></span>
                		Education 
                		<span className="icon-education pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-summary mr-10"></span>
                		Skills 
                		<span className="icon-skills pull-right"></span>
                	</li>
                </ul>
            </div>
        )
    }

}