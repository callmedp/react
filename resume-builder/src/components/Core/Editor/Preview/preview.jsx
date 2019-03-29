import React ,{Component} from 'react';
import './preview.scss'
export default class Preview extends Component {
    render(){
        return(
            <div className="preview-section">
                <strong>Complete your customisation</strong>
                <div className="preivew-scroll">
	                <div className="change-theme">
	                	<a href="#" className="change-theme--theme-heading change-theme--active">
	                		<span className="icon-change-theme mr-20"></span>
		                    Change theme
	                	</a>
	                	<ul className="change-theme-content">
	                		<li>
	                			<input type="radio" name="radio1" id="green" value="green" />
	                			<label for="green"><span className="theme-green"></span></label>
	                		</li>
	                		<li>
	                			<input type="radio" name="radio1" id="blue" value="blue" />
	                			<label for="blue"><span className="theme-blue"></span></label>
	                		</li>
	                		<li>
	                			<input type="radio" name="radio1" id="red" value="red"/>
	                			<label for="red"><span className="theme-red"></span></label>
	                		</li>
	                		<li>
	                			<input type="radio" name="radio1" id="black" value="black" />
	                			<label for="black"><span className="theme-black"></span></label>
	                		</li>
	                		<li>
	                			<input type="radio" name="radio1" id="brown" value="brown"/>
	                			<label for="brown"><span className="theme-brown"></span></label>
	                		</li>
	                		<li>
	                			<input type="radio" name="radio1" id="violet" value="violet" />
	                			<label for="violet"><span className="theme-violet"></span></label>
	                		</li>
	                	</ul>
	                </div>
	                <div className="change-theme">
	                	<a href="#" className="change-theme--theme-heading change-theme--active">
	                		<span className="icon-change-font mr-20"></span>
		                    Font size
	                	</a>
	                	<ul className="change-font-content">
	                		<li>
	                			<strong>Section Heading</strong>
	                			<div className="change-font-content--font-box">
	                				<div role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" className="change-font-content--font-bar">
					                  <span className="change-font-content--font-bar__bar"></span>
					                </div>
	                			</div>
	                			<div className="change-font-content--text-align">
	                				<span>S</span> 
	                				<span>M</span> 
	                				<span>L</span>
	                			</div>
	                		</li>
	                		<li>
	                			<strong>Section Text</strong>
	                			<div className="change-font-content--font-box">
	                				<div role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" className="change-font-content--font-bar">
					                  <span className="change-font-content--font-bar__bar"></span>
					                </div>
					                <div className="change-font-content--text-align">
		                				<span>S</span> 
		                				<span>M</span> 
		                				<span>L</span>
		                			</div>
	                			</div>
	                		</li>
	                	</ul>
	                </div>
	                <div className="change-theme">
	                	<a href="#" className="change-theme--theme-heading">
	                		<span className="icon-change-reorder mr-20"></span>
		                    Reorder section
	                	</a>
	                	<ul className="reorder-content">
	                		<li className="reorder-content--select-box reorder-content--select-box__select">
	                			Personal Info
	                			<span className="addon-buttons">
	                				<span className="icon-ascend mr-5 ml-0"></span>
	                				<span className="icon-descend ml-0"></span>
	                			</span>
	                		</li>
	                		<li className="reorder-content--select-box">Summary</li>
	                		<li className="reorder-content--select-box">Experience</li>
	                		<li className="reorder-content--select-box">Education</li>
	                		<li className="reorder-content--select-box">Skills</li>
	                	</ul>
	                </div>
	            </div>
               <button className="orange-button preview-section__orange-button mt-40">Get your resume</button>
            </div>
        )
    }

}