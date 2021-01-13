import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import '../../SkillPage/NeedHelp/needHelp.scss';
import './myProfile.scss';
import '../../SkillPage/NeedHelp/needHelp.scss';

   
const MyProfile = (props) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const [skillsShow, setSkillsShow] = useState(false);
    const handleSkillsClose = () => setSkillsShow(false);
    const handleSkillsShow = () => setSkillsShow(true);



    return(
        <div className="myProfile">

            <div className="db-white-box w-100 d-flex">
                <div className="myProfile__leftpan mt-10">
                    <span className="myProfile__leftpan--shortName">AK</span>

                    <div className="myProfile__leftpan--wrap">
                        <h1>Amit Kumar</h1>
                        <p>Sr. Sales manager </p>

                        <ul className="myProfile__leftpan--personInfo mt-20 mb-20">
                            <li className="db-mail">amit.kumar123@gmail.com 
                                <Link to={"#"} className="font-weight-bold ml-3">Verify</Link>
                            </li>

                            <li className="db-mobile">9876543212 
                                <Link to={"#"} className="font-weight-bold ml-3">Verify</Link>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="myProfile__rightpan">
                    <div className="db-status mt-20">
                        <p className="mb-0 pb-1">Profile Status: <strong>(50% Complete)</strong> </p>
                        <ProgressBar now={50} />
                        <p className="last-update">Last update: 23 jan 2020</p>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Personal</h2>
                    <div className="col-3 text-right">
                        <button 
                            className="btn btn-link text-center"
                            onClick={handleShow}
                        >
                                <i className="db-edit-icon"></i>
                        </button>
                    </div>
                </div>

                <div className="row">
                    <ul className="col-6 myProfile--detail">
                        <li>
                            <strong>Name</strong>
                            Amit Kumar
                        </li>
                        <li>
                            <strong>Mobile</strong>
                            9871234566
                        </li>
                        <li>
                            <strong>Email</strong>
                            amitkumar123@gmail.com
                        </li>
                        <li>
                            <strong>Password</strong>
                            <Link className="font-weight-bold">Change Password </Link>
                        </li>
                    </ul>
                    
                    <ul className="col-6 myProfile--detail">
                        <li>
                            <strong>Date of Birth</strong>
                            10 june 1991
                        </li>
                        <li>
                            <strong>Location</strong>
                            New Delhi
                        </li>
                        <li>
                            <strong>Email</strong>
                            amitkumar123@gmail.com
                        </li>
                        <li>
                            <strong>Gender</strong>
                            Male
                        </li>
                    </ul>
                </div>
                
                <Modal show={show} onHide={handleClose} className="edit-view">
                    <Modal.Header closeButton></Modal.Header>
                    <Modal.Body>
                        <strong className="d-block heading-fs-16">Edit personal info</strong>
                        <div className="edit-form need-help">
                            <form action="">
                                <ul>
                                    <li>
                                        <div className="form-group error">
                                            <input type="text" className="form-control" id="name" name="name" value="Amit Kumar" placeholder=" " aria-required="true" aria-invalid="true" />
                                            <label for="">Name</label>
                                            <span class="error-msg">Required</span>
                                        </div>

                                        <div className="form-group">
                                            <input type="text" className="form-control" id="mobile" name="mobile" placeholder=" "
                                                value="9871234567" aria-required="true" aria-invalid="true" />
                                            <label for="">Mobile</label>
                                        </div>

                                        <div className="form-group">
                                            <input type="email" className="form-control" id="email" name="email" placeholder=" "
                                                value="amit.kumar123@gmail.com" aria-required="true" aria-invalid="true" />
                                            <label for="">Email</label>
                                        </div>
                                        
                                        <div className="form-group password">
                                            <input type="password" className="form-control" id="password" name="password" placeholder=" " value="xxxxxxxxxxxxxx" aria-required="true" aria-invalid="true" />
                                            <label for="">Password</label>
                                            <Link className="db-eye-icon"></Link>
                                            <Link to={"#"} className="font-weight-bold d-block text-right mt-1">Change</Link>
                                        </div>

                                        <div className="form-group">
                                            <button className="btn btn-primary px-5">Save</button>
                                        </div>
                                    </li>

                                    <li>
                                        <div className="form-group">
                                            <input type="text" className="form-control" id="dob" name="dob" placeholder=" "
                                                value="DD/MM/YY" aria-required="true" aria-invalid="true" />
                                            <label for="">DOB</label>
                                        </div>

                                        <div className="form-group">
                                            <select class="form-control" id="exampleFormControlSelect1">
                                                <option>1</option>
                                                <option>2</option>
                                                <option>3</option>
                                                <option>4</option>
                                                <option>5</option>
                                            </select>
                                        </div>

                                        <div className="form-group">
                                            <strong className="d-block">Select gender</strong>
                                            <div className="db-custom-select-form">
                                                <div className="custom-control custom-radio mb-10">
                                                    <input type="radio" id="male" name="selectGender" className="custom-control-input" />
                                                    <label className="custom-control-label" for="male"> Male</label>
                                                </div>
                                                
                                                <div className="custom-control custom-radio mb-10">
                                                    <input type="radio" id="female" name="selectGender" className="custom-control-input" />
                                                    <label className="custom-control-label" for="female"> Male</label>
                                                </div>
                                                
                                                <div className="custom-control custom-radio mb-10">
                                                    <input type="radio" id="binary" name="selectGender" className="custom-control-input" />
                                                    <label className="custom-control-label" for="binary"> Non- Binary</label>
                                                </div>
                                                
                                                <div className="custom-control custom-radio mb-10">
                                                    <input type="radio" id="prefer" name="selectGender" className="custom-control-input" />
                                                    <label className="custom-control-label" for="prefer"> Prefer not to say</label>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </form>
                        </div>
                    </Modal.Body>
                </Modal>

            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Resume</h2>
                    <div className="col-3 text-right">
                        <div class="upload-btn-wrapper">
                            <button class="btn btn-outline-primary">Upload new resume</button>
                            <input type="file" name="myfile" />
                        </div>
                    </div>
                </div>

                <div className="db-custom-select-form">
                    <div class="custom-control custom-radio mb-10">
                        <input type="radio" id="dResume" name="resume" class="custom-control-input" />
                        <label class="custom-control-label" for="dResume">
                            <Link to={"#"} className="font-weight-bold mr-2">Newresume25-May.doc</Link>
                            (Default resume)
                        </label>
                    </div>

                    <div class="custom-control custom-radio">
                        <input type="radio" id="resume" name="resume" class="custom-control-input" />
                        <label class="custom-control-label" for="resume">
                            <Link to={"#"} className="font-weight-bold mr-2">Salemanagerresume.doc</Link>
                        </label>
                    </div>
                </div>
            </div>

            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Overview</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-link text-center"><i className="db-edit-icon"></i></button>
                    </div>
                </div>

                <div className="row">
                    <ul className="col-6 myProfile--detail">
                        <li>
                            <strong>Profile title</strong>
                            Sales Manager, Sapient
                        </li>
                        <li>
                            <strong>Total Experience</strong>
                            3 yrs
                        </li>
                        <li>
                            <strong>Current Salary</strong>
                            Rs. 5.00 Lacs
                        </li>
                    </ul>
                    
                    <ul className="col-6 myProfile--detail">
                        <li>
                            <strong>Profile summary</strong>
                            Curabitur in nisi dictum ante euismod
                        </li>
                        <li>
                            <strong>Team handled</strong>
                            5
                        </li>
                        <li>
                            <strong>Notice period</strong>
                            60 Days
                        </li>
                    </ul>
                </div>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Experience</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <div className="myProfileAdd">
                    <div className="myProfileAdd__rightwrap">
                        <span className="myProfileAdd__rightwrap--iconCircle db-experience"></span>
                        <h3>Sales Manager</h3>
                        <p>Wipro, Gurgaon</p>
                        <p className="myProfileAdd__rightwrap--duration"><span>2012 May - Present</span>  <span>4 yrs  6 month</span></p>

                        <p className="myProfileAdd__rightwrap--info">
                            <strong>Functional area</strong>
                            <span>Application Programming</span><span>Client Server</span>
                        </p>   

                        <p className="myProfileAdd__rightwrap--info">
                            <strong>Industry</strong>
                            IT - Software
                        </p>   
                    </div>

                    <div className="myProfileAdd__leftwrap pt-20">
                        <button className="btn btn-link text-center mr-3"><i className="db-edit-icon"></i></button>
                        <Link className="bd-btn-close"></Link>
                    </div>
                </div>
                
                <div className="myProfileAdd">
                    <div className="myProfileAdd__rightwrap">
                        <span className="myProfileAdd__rightwrap--iconCircle db-experience"></span>
                        <h3>Sr. Sales Manager</h3>
                        <p>Sapient, Gurgaon</p>
                        <p className="myProfileAdd__rightwrap--duration"><span>2012 May - Present</span>  <span>4 yrs  6 month</span></p>

                        <p className="myProfileAdd__rightwrap--info">
                            <strong>Functional area</strong>
                            <span>Application Programming</span><span>Client Server</span>
                        </p>   

                        <p className="myProfileAdd__rightwrap--info">
                            <strong>Industry</strong>
                            IT - Software
                        </p>   
                    </div>

                    <div className="myProfileAdd__leftwrap pt-20">
                        <button className="btn btn-link text-center mr-3"><i className="db-edit-icon"></i></button>
                        <Link className="bd-btn-close"></Link>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Experience</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <p>You havn’t added any work experience. Get customised job recommendation by adding experience</p>

            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Education</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <div className="myProfileAdd">
                    <div className="myProfileAdd__rightwrap">
                        <span className="myProfileAdd__rightwrap--iconCircle db-education"></span>
                        <h3>MBA</h3>
                        <p className="myProfileAdd__rightwrap--name">Indian Institute of Management, Bangalore</p>
                        <p className="myProfileAdd__rightwrap--duration"><span>Correspondence</span>  <span>2016 - 2018</span></p>  
                    </div>

                    <div className="myProfileAdd__leftwrap pt-20">
                        <button className="btn btn-link text-center mr-3"><i className="db-edit-icon"></i></button>
                        <Link className="bd-btn-close"></Link>
                    </div>
                </div>
                
                <div className="myProfileAdd">
                    <div className="myProfileAdd__rightwrap">
                        <span className="myProfileAdd__rightwrap--iconCircle db-education"></span>
                        <h3>Bachelor of Commerce</h3>
                        <p className="myProfileAdd__rightwrap--name">Delhi University</p>
                        <p className="myProfileAdd__rightwrap--duration"><span>Full time</span>  <span>2013 - 2016</span></p>  
                    </div>

                    <div className="myProfileAdd__leftwrap pt-20">
                        <button className="btn btn-link text-center mr-3"><i className="db-edit-icon"></i></button>
                        <Link className="bd-btn-close"></Link>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Education</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <p>By adding your education you will be able to get expert recommendation for your career</p>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Skills</h2>
                    <div className="col-3 text-right">
                        <button 
                            className="btn btn-outline-primary"
                            onClick={handleSkillsShow}
                        >Add/ Edit
                        </button>
                    </div>
                </div>

                <div className="skills-tag">
                    <span>Data Science</span>
                    <span>ERP Management</span>
                    <span>Six Sigma</span>
                </div>
                <Modal show={skillsShow} onHide={handleSkillsClose}>
                    <Modal.Header closeButton></Modal.Header>
                    <Modal.Body>
                        <strong className="d-block heading-fs-16">Add skills</strong>
                        <div className="need-help mt-30">
                            <form action="">
                                <div className="form-group">
                                    <input type="text" className="form-control" id="mobile" name="mobile" placeholder=" "
                                        value="Data Science" aria-required="true" aria-invalid="true" />
                                    <label for="">Skills</label>
                                </div>

                                <div className="skills-tag add-skill">
                                    <span>Data Science</span>
                                    <span>ERP Management</span>
                                    <span>Six Sigma</span>
                                </div>

                                <button className="btn btn-primary px-5 mt-30">Save</button>
                            </form>
                        </div>
                    </Modal.Body>
                </Modal>
            </div>

            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Skills</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <p>You have not added any skiils</p>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Certification</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <div className="myProfileAdd">
                    <div className="myProfileAdd__rightwrap">
                        <span className="myProfileAdd__rightwrap--iconCircle db-certification"></span>
                        <h3>Six Sigma Green Belt Professional</h3>
                        <p className="myProfileAdd__rightwrap--duration"><span>By Edureka</span>  <span>Dec. 2014</span></p>  
                    </div>

                    <div className="myProfileAdd__leftwrap">
                        <button className="btn btn-link text-center mr-3"><i className="db-edit-icon"></i></button>
                        <Link className="bd-btn-close"></Link>
                    </div>
                </div>
            </div>
            
            <div className="db-white-box w-100 pt-20 pb-30">
                <div className="row mb-10">
                    <h2 className="col-9">Certification</h2>
                    <div className="col-3 text-right">
                        <button className="btn btn-outline-primary">Add New</button>
                    </div>
                </div>

                <p>Add certification in your profile to get expert recommendations</p>
            </div>

        </div>
    )
}
   
export default MyProfile;