import React, {Component} from 'react';
import './personalInfo.scss'

export default class PersonalInfo extends Component {
    render() {
        return (
        <div>
            <section className="head-section">
	             <span className="icon-box"><i className="icon-info1"></i></span>
	             <h2>Personal Info</h2>
	             <span className="icon-edit icon-edit__cursor"></span>
        	</section>
        	
        	<section className="flex-container right-sidebar-scroll">
        		<section className="info-section">
	        		<div className="flex-container">
	        			<fieldset className="error">
		        			<label>First Name</label>
		        			<input type="text" name="" placeholder="" />
		        			<span class="error-txt"></span>
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
							<div className="input-group">
								<div className="input-group--input-group-icon">
							  		<span className="icon-mobile"></span>
								</div>
								<input type="text" placeholder="" className="input-control" />
							</div>
		        		</fieldset>
		        		<fieldset>
	        				<label>Email</label>
							<div className="input-group">
								<div className="input-group--input-group-icon">
							  		<span className="icon-email"></span>
								</div>
								<input type="text" placeholder="" className="input-control" />
							</div>
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
	        				<label>Address</label>
							<div className="input-group">
								<div className="input-group--input-group-icon">
							  		<span className="icon-address"></span>
								</div>
								<input type="text" placeholder="" className="input-control" />
							</div>
		        		</fieldset>
	        		</div>
	        		<div className="flex-container">
	        			<fieldset>
	        				<label>Linkedin</label>
							<div className="input-group">
								<div className="input-group--input-group-icon">
							  		<span className="icon-linkedin"></span>
								</div>
								<input type="text" placeholder="" className="input-control" />
							</div>
		        		</fieldset>
		        		<fieldset>
	        				<label>Facebook</label>
							<div className="input-group">
								<div className="input-group--input-group-icon">
							  		<span className="icon-facebook"></span>
								</div>
								<input type="text" placeholder="" className="input-control" />
							</div>
		        		</fieldset>
	        		</div>


	        	</section>

	        	<section className="pic-section mt-30">
	        		<img className="img-responsive" src="/images/upload-image.jpg" />
	        	</section>
        	</section>

        	<div class="flex-container items-right mr-20 mb-30">
        		<button className="blue-button mr-10">Preview</button>
        		<button className="orange-button">Save & Continue</button>
        	</div>
        	
        </div>
        )
    }
}