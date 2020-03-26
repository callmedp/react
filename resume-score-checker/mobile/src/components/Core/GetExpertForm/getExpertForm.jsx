import React from 'react';
import './getExpertForm.scss';
import { Link } from 'react-router-dom';


export default function GetExpertForm() {
    return(
        <div className="getExpertForm">
            <div className="getExpertForm__header">
                <Link to = "/score-checker"><span className="sprite back-icon"></span></Link>
                <strong className="ml-15">Get Help</strong>
            </div>

            <div className="container-box">
                <p className="getExpertForm__head">Fill the form below to get help</p>
                <form action="" className="getExpertForm__form">
                    <ul>
                        <li class="form-group">
                            <div class="floating-label">      
                                <input class="form--control floating-input" type="text" placeholder=" " />
                                <label>Name</label>
                            </div>
                            {/* <span class="error--mgs">Name</span> */}
                        </li>   

                        <li class="form-group">
                            <div class="floating-label">      
                                <input class="form--control floating-input" type="text" placeholder=" " />
                                <label>Email ID</label>
                            </div>
                        </li>                 

                        <li class="getExpertForm__number form-group d-flex">
                            <div class="code">
                                <select class="form--control floating-select">
                                    <option value="+91">+91</option>
                                    <option value="+92">+92</option>
                                    <option value="+2345">+2345</option>
                                    <option value="+9834">+9834</option>
                                </select>
                            </div>

                            <div class="number"> 
                                <div class="floating-label">      
                                    <input class="form--control floating-input" type="text" placeholder=" " />
                                    <label>Number</label>
                                </div>
                            </div>
                        </li>


                        

                        <li>
                            <button className="btn btn-round-30 btn-blue w-100">Submit</button>
                        </li>
                    </ul>
                </form>
            </div>
        </div>
    );
}