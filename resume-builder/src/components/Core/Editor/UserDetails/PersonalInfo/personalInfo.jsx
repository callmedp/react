import React, {Component} from 'react';
import './personalInfo.scss'

export default class PersonalInfo extends Component {
    render() {
        return (
        <div>
            <section className="head-section">
	             <span className="icon-box"><i className="icon-info1"></i></span>
	             <h2>Personal Info</h2>
	             <span className="icon-edit"></span>
        	</section>
        	
        	<section className="flex-container">
        		<section className="info-section">
	        		<div className="flex-container">
	        			<fieldset>
		        			<label>First Name</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
		        		<fieldset>
		        			<label>Last Name</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
		        			<label>Designation</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
		        		<fieldset>
		        			<label>Company</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
		        			<label>Mobile</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
		        		<fieldset>
		        			<label>Email</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
		        			<label>Address</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
		        			<label>Linkedin</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
		        		<fieldset>
		        			<label>Facebook</label>
		        			<input type="text" name="" placeholder="" />
		        		</fieldset>
	        		</div>
	        	</section>

	        	<section className="pic-section">
	        		<img src="/images/upload-image.jpg" />
	        	</section>
        	</section>
        	
        </div>
        )
    }
}