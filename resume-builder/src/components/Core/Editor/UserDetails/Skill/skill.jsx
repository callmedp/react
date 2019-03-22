import React, {Component} from 'react';
import './skill.scss'


export default class Skill extends Component {
    render() {
        return (
            <div>
            	<section className="head-section">
		             <span className="icon-box"><i className="icon-skills1"></i></span>
		             <h2>Skills</h2>
		             <span className="icon-edit icon-education__cursor"></span>
		             <button className="add-button add-button__right">Add new</button>
	        	</section>

	        	<section className="right-sidebar-scroll">
        			<section className="info-section">
        				<div className="flex-container">
		        			<h3 class="add-section-heading">Skill1</h3>
		        			<div className="addon-buttons mr-10">
		        				<span className="icon-delete mr-15"></span>
		        				<span className="icon-ascend mr-5"></span>
		        				<span className="icon-descend"></span>
		        			</div>
		        		</div>
		        		<div className="flex-container">
		        			<fieldset className="width-half">
			        			<label>Skill name</label>
			        			<input type="text" name="" placeholder="" />			        			
			        		</fieldset>
			        		
			        		<fieldset className="width-half">
			        			<label>Skill rating (out of 10)</label>
			        			<span className="styled-select">
				        			<select selected>
				        				<option></option>
				        				<option>1</option>
				        				<option>2</option>
				        				<option>3</option>
				        			</select>	
			        			</span>		        			
			        		</fieldset>
		        		</div>

		        	</section>


	        	</section>

	        	<div className="flex-container items-right mr-20 mb-30">
	        		<button className="blue-button mr-10">Preview</button>
	        		<button className="orange-button">Save & Continue</button>
	        	</div>

	        </div>
        )
    }
}