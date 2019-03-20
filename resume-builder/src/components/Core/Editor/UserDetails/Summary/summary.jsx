import React, {Component} from 'react';
import './summary.scss'


export default class Summary extends Component {
    render() {
        return (
            <div>
            	<section className="head-section">
		             <span className="icon-box"><i className="icon-summary1"></i></span>
		             <h2>Summary</h2>
		             <span className="icon-edit icon-summary__cursor"></span>
	        	</section>

	        	<section className="flex-container p3p">
	        		<div className="summary-box">
	        			<h3>Summary</h3>
	        			<div className="summary-box--summary-txt">
	        				Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
	        			</div>
	        		</div>

	        	</section>

	        	<div class="flex-container items-right mr-20 mb-30">
	        		<button className="blue-button mr-20">Preview</button>
	        		<button className="orange-button">Save & Continue</button>
	        	</div>

            </div>
        )
    }
}