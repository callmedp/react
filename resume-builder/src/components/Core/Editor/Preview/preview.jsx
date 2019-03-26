import React ,{Component} from 'react';
import './preview.scss'
export default class Preview extends Component {
    render(){
        return(
            <div className="preview-section">
                <strong>Complete your customisation</strong>
                <div className="change-theme">
                	<a href="#" className="change-theme--theme-heading change-theme--active">
                		<span className="icon-change-theme mr-20"></span>
	                    Change theme
                	</a>
                	<ul className="change-theme-content">
                		<li></li>
                	</ul>
                </div>
                <div className="change-theme">
                	<a href="#" className="change-theme--theme-heading">
                		<span className="icon-change-font mr-20"></span>
	                    Font size
                	</a>
                	<ul className="change-theme-content hidden">
                		<li></li>
                	</ul>
                </div>
                <div className="change-theme">
                	<a href="#" className="change-theme--theme-heading">
                		<span className="icon-change-reorder mr-20"></span>
	                    Reorder section
                	</a>
                	<ul className="change-theme-content hidden">
                		<li></li>
                	</ul>
                </div>
               <button className="orange-button preview-section__orange-button mt-40">Get your resume</button>
            </div>
        )
    }

}