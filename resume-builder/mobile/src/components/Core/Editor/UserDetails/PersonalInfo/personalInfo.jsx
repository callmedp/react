import React, {Component} from 'react';

export default class PersonalInfo extends Component {
    render() {
        return (
        <div className="buildResume">
            <div className="buildResume__wrap">
                <div className="buildResume__heading">
                    <h2>Personal Info</h2>
                    <i className="sprite icon--edit"></i>
                </div>

                <ul className="form">
                    <li className="form__group">
                        <label className="form__label" for="firstName">First Name</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--firstName"></i>
                            </span>
                            </div>
                            <input type="text" name="firstName" className="form__input" placeholder="Amit" aria-label="firstName" id="firstName" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="lastName">Last Name</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--lastName"></i>
                            </span>
                            </div>
                            <input type="text" name="lastName" className="form__input" placeholder="Sinha" aria-label="lastName" id="lastName" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="designation">Designation</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--designation"></i>
                            </span>
                            </div>
                            <input type="text" name="designation" className="form__input" placeholder="IT Project Manager" aria-label="designation" id="designation" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="company">Company</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--company"></i>
                            </span>
                            </div>
                            <input type="text" name="company" className="form__input" placeholder="Sapient" aria-label="company" id="company" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="mobile">Mobile</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--mobile"></i>
                            </span>
                            </div>
                            <input type="tel" name="mobile" className="form__input" placeholder="" aria-label="Mobile" id="mobile" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="email">Email</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--mail"></i>
                            </span>
                            </div>
                            <input type="email" name="email" className="form__input" placeholder="amit.sinha@gmail.com" aria-label="email" id="email" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="address">Address</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--address"></i>
                                </span>
                            </div>

                            <textarea row="4" name="address" className="form__input" placeholder="Address" aria-label="address" id="address" ></textarea>
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="linkedin">Linkedin</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--linkedin"></i>
                            </span>
                            </div>
                            <input type="text" name="linkedin" className="form__input" placeholder="amit.sinha@gmail.com" aria-label="linkedin" id="linkedin" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <label className="form__label" for="facebook">Facebook</label>
                        <div className="input-group">
                            <div className="input-group__prepend">
                            <span className="input-group__text">
                                <i className="sprite icon--facebook"></i>
                            </span>
                            </div>
                            <input type="text" name="facebook" className="form__input" placeholder="amit.sinha@gmail.com" aria-label="facebook" id="facebook" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <div class="upload-btn-wrapper">
                            
                            <button class="upload-btn-wrapper__btn">
                                <i className="sprite icon--camera"></i>
                                Upload a file
                            </button>
                            <input type="file" name="myfile" />
                        </div>
                    </li>
                    
                    <li className="form__group">
                        <span className="upload--image">
                            <img src="/images/default-user.jpg" />  
                        </span>
                    </li>

                    <li className="form__group">
                        <div className="btn-wrap">
                            <button className="btn btn__round btn--outline">Preview</button>
                            <button className="btn btn__round btn__primary">Save &amp; Continue</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        )
    }
}