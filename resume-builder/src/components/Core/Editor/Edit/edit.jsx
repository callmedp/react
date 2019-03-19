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
                	</li>
                	<li>
                		<span className="icon-summary mr-10"></span>
                		Summary 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-experience mr-10"></span>
                		Experience 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-education mr-10"></span>
                		Education 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li>
                		<span className="icon-skills mr-10"></span>
                		Skills 
                		<span className="icon-delete pull-right"></span>
                	</li>
                	<li className="edit-section--addmore">
                		+ Add more sections
                	</li>
                	<li className="">
                		<span className="icon-languages mr-10"></span>
                		Languages 
                		<span className="icon-add pull-right"></span>
                	</li>
                	<li className="hidden">
                		<span className="icon-awards mr-10"></span>
                		Awards 
                		<span className="icon-add pull-right"></span>
                	</li>
                	<li className="hidden">
                		<span className="icon-courses mr-10"></span>
                		Courses 
                		<span className="icon-add pull-right"></span>
                	</li>
                	<li className="hidden">
                		<span className="icon-projects mr-10"></span>
                		Projects 
                		<span className="icon-add pull-right"></span>
                	</li>
                	<li className="hidden">
                		<span className="icon-references mr-10"></span>
                		References 
                		<span className="icon-add pull-right"></span>
                	</li>

                </ul>
            </div>
        )
    }

}