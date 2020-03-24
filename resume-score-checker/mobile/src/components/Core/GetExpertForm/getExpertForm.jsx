import React from 'react';
import './getExpertForm.scss';


export default function GetExpertForm() {
    return(
        <div className="getExpertForm">
            <div className="getExpertForm__header">
                <span className="sprite back-icon"></span>
                <strong>Get Help</strong>
            </div>

            <div className="container-box">
                <form action="" className="getExpertForm__form">
                    <ul>
                        <li class="form-group input-effect">
                            <input type="text" id="name" name="name" value="{{request.session.full_name}}" 
                                class="form--control animation-input {% if request.session.full_name %}has-content{% endif %}" 
                                placeholder=""></input>
                            <label for="name">Name</label>
                            <span class="error--mgs">Name</span>
                        </li>

                        <li class="form-group d-flex">
                            <div class="input-effect code">
                                <select name="country_code" class="form-control" id="country-code">
                                    
                                </select>
                            </div>
                            <div class="input-effect ml-auto number-w67 pr"> 
                                <input type="text"  name="number"
                                    class="form--control animation-input" 
                                    placeholder=""></input>
                                <label for="mobile-id">Mobile</label>
                                <span class="error--mgs"></span>
                            </div>
                        </li>

                        <li class="form-group input-effect">
                            <input type="email" name="email" id="email-id" value="{{request.session.email}}"   
                                class="form--control animation-input {% if request.session.email %}has-content{% endif %}"
                                aria-describedby="email-id" placeholder=""></input>
                            <label for="email-id">Email id</label>
                            <span class="error--mgs"></span>
                        </li>
                    </ul>
                </form>
            </div>
        </div>
    );
}