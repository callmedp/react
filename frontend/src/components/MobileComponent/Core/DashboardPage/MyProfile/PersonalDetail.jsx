import React from 'react';
import { Link } from 'react-router-dom';
import './personalDetail.scss';

const PersonalDetail = (props) => {
    return(
        <div className="personal-detail">
            <div className="personal-detail__heading">
                <button className="m-db-btn-close"></button>
                <h2>Personal details</h2>
                <Link to={"#"} className="personal-detail__heading--save">Save</Link>
            </div>

            <div className="m-container">
                <div className="m-enquire-now personal-detail__form">
                    <ul>
                        <li className="m-form-group">
                            <input type="text" id="name" className="m-form-control" name="name"  placeholder=" " aria-required="true" aria-invalid="true" value="Amit Kumar" />
                            <label className="input-label" for="">Name</label>
                        </li>
                        
                        <li className="m-form-group">
                            <input type="number" className="m-form-control" id="mobile" name="mobile"  placeholder=" " aria-required="true" aria-invalid="true" value="9871234567" />
                            <label className="input-label" for="">Mobile</label>
                        </li>
                        
                        <li className="m-form-group">
                            <input type="email" className="m-form-control" id="email" name="email"  placeholder=" " aria-required="true" aria-invalid="true" value="amit.kumar123@gmail.com" />
                            <label className="input-label" for="">Email</label>
                        </li>
                        
                        <li className="m-form-group">
                            <input type="text" className="m-form-control" id="dob" name="dob"  placeholder=" " aria-required="true" aria-invalid="true" value="DD/MM/YY" />
                            <label className="input-label" for="">DOB</label>
                        </li>
                        
                        <li className="m-form-group">
                            <select class="m-form-control" id="exampleFormControlSelect1">
                                <option>New Delhi</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                                <option>5</option>
                            </select>
                        </li>
                        
                        <li className="m-form-group m-password">
                            <input type="password" className="m-form-control" id="password" name="password" placeholder=" " value="xxxxxxxxxxxxxx" aria-required="true" aria-invalid="true" />
                            <label className="input-label" for="">Password</label>
                            <Link className="m-db-eye-icon"></Link>
                            <Link to={"#"} className="font-weight-bold d-block text-right mt-10 fs-12">Change</Link>
                        </li>

                        <li className="form-group">
                            <strong className="d-block mb-5">Select gender</strong>

                            <div className="personal-detail__form--gender">
                                <div className="m-custom">
                                    <input type="radio" id="male" name="gender" /> 
                                    <label htmlFor="male">Male</label>
                                </div>
                                
                                <div className="m-custom">
                                    <input type="radio" id="female" name="gender" /> 
                                    <label htmlFor="female">Female</label>
                                </div>
                                
                                <div className="m-custom">
                                    <input type="radio" id="binary" name="gender" /> 
                                    <label htmlFor="binary">Non- Binary</label>
                                </div>
                                
                                <div className="m-custom">
                                    <input type="radio" id="prefer" name="gender" /> 
                                    <label htmlFor="prefer">Prefer not to say</label>
                                </div>
                            </div>

                           
                        </li>
                    </ul>
                </div>
            </div>

            

            
        </div>
    )

}

export default PersonalDetail;