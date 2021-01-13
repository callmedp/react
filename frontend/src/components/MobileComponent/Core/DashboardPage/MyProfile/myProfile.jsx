import React from 'react';
import { Link } from 'react-router-dom';
import './myProfile.scss';

   
const MyProfile = (props) => {
    return(
        <div className="db-warp m-myProfile">
            <div className="m-card m-profileFirst-card">
                <div className="m-myProfile__leftpan">
                    <span className="m-myProfile__leftpan--shortName">AK</span>

                    <div className="m-myProfile__leftpan--wrap">
                        <h1>Amit Kumar</h1>
                        <p>Sr. Sales manager </p>

                    
                        <div className="m-db-status">
                            <p className="mb-0 pb-1">Profile Status: <strong>(50% Complete)</strong> </p>

                            <div class="m-progress">
                                <div role="progressbar" class="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "50%"}}></div>
                            </div>
                            <p className="fs-10 mb-0">Last update: 23 jan 2020</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Personal</h2>
                    <Link to={"#"}><i className="m-db-edit-icon"></i></Link>
                </div>

                <ul className="m-myProfile--detail">
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
            
            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Resume</h2>
                </div>
                <div class="m-custom mb-10">
                    <input type="radio" id="dResume" name="resume" />
                    <label for="dResume">
                        <Link to={"#"} className="font-weight-bold mr-10">Newresume25-May.doc</Link>
                        (Default resume)
                    </label>
                </div>

                <div class="m-custom">
                    <input type="radio" id="resume" name="resume" />
                    <label for="resume">
                        <Link to={"#"} className="font-weight-bold mr-10">Salemanagerresume.doc</Link>
                    </label>
                </div>

                <div class="m-upload-btn-wrapper mt-30">
                    <button class="btn-blue-outline">Upload new resume</button>
                    <input type="file" name="myfile" />
                </div>
            </div>

            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Overview</h2>
                    <Link to={"#"}><i className="m-db-edit-icon"></i></Link>
                </div>

                <ul className="m-myProfile--detail">
                    <li>
                        <strong>Profile title</strong>
                        Not Mentioned
                    </li>
                    <li>
                        <strong>Total Experience</strong>
                        3 yrs
                    </li>
                    <li>
                        <strong>Current Salary</strong>
                        Rs. 5.00 Lacs
                    </li>
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


            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Experience</h2>
                    <button className="btn-xs btn-blue-outline ">Add New</button>
                </div>

                <div className="m-myProfileAdd">
                    <span className="m-myProfileAdd--iconCircle m-db-experience"></span>

                    <div className="m-myProfileAdd__info">
                        <div className="m-myProfileAdd__info--heading">
                            <div>
                                <h3>Sales Manager</h3>
                                <p>Wipro, Gurgaon</p>
                            </div>

                            <div className="m-myProfileAdd__info--action">
                                <Link className="mr-15"><i className="db-edit-icon"></i></Link>
                                <Link className="m-db-btn-close"></Link>
                            </div>
                        </div>
                        <p className="m-myProfileAdd__info--duration">
                            <span className="infoItem">2012 May - Present</span>  <span className="infoItem">4 yrs  6 month</span>
                        </p>

                        <div className="m-myProfileAdd__info--info mb-10">
                            <strong>Functional area</strong>

                            <div className="m-myProfileAdd__info--content">
                                <span>Application Programming</span><span>Client Server</span>
                            </div>
                        </div>   

                        <p className="m-myProfileAdd__info--info mb-0">
                            <strong>Industry</strong>
                            IT - Software
                        </p> 
                    </div>
                </div>
                
                <div className="m-myProfileAdd">
                    <span className="m-myProfileAdd--iconCircle m-db-experience"></span>

                    <div className="m-myProfileAdd__info">
                        <div className="m-myProfileAdd__info--heading">
                            <div>
                                <h3>Sr. Sales Manager</h3>
                                <p>Sapient, Gurgaon</p>
                            </div>

                            <div className="m-myProfileAdd__info--action">
                                <Link className="mr-15"><i className="db-edit-icon"></i></Link>
                                <Link className="m-db-btn-close"></Link>
                            </div>
                        </div>
                        <p className="m-myProfileAdd__info--duration">
                            <span className="infoItem">2012 May - Present</span>  <span className="infoItem">4 yrs  6 month</span>
                        </p>

                        <div className="m-myProfileAdd__info--info mb-10">
                            <strong>Functional area</strong>

                            <div className="m-myProfileAdd__info--content">
                                <span>Application Programming</span><span>Client Server</span>
                            </div>
                        </div>   

                        <p className="m-myProfileAdd__info--info mb-0">
                            <strong>Industry</strong>
                            IT - Software
                        </p> 
                    </div>
                </div>
            </div>

            <div className="m-card">
                <h2>Experience</h2>
                <p>You havn’t added any work experience. Get customised job recommendation by adding experience</p>
                <button className="btn-xs btn-blue-outline ">Add New</button>
            </div>
            
            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Education</h2>
                    <button className="btn-xs btn-blue-outline ">Add New</button>
                </div>

                <div className="m-myProfileAdd">
                    <span className="m-myProfileAdd--iconCircle m-db-education"></span>

                    <div className="m-myProfileAdd__info">
                        <div className="m-myProfileAdd__info--heading">
                            <div>
                                <h3>MBA</h3>
                                <p>Indian Institute of Management, Gurgaon</p>
                            </div>

                            <div className="m-myProfileAdd__info--action">
                                <Link className="mr-15"><i className="db-edit-icon"></i></Link>
                                <Link className="m-db-btn-close"></Link>
                            </div>
                        </div>
                        <p className="m-myProfileAdd__info--duration">
                            <span className="infoItem">Correspondence</span>  <span className="infoItem">2016 - 2018</span>
                        </p>  
                    </div>
                </div>
                
                <div className="m-myProfileAdd">
                    <span className="m-myProfileAdd--iconCircle m-db-education"></span>

                    <div className="m-myProfileAdd__info">
                        <div className="m-myProfileAdd__info--heading">
                            <div>
                                <h3>Bachelor of Commerce</h3>
                                <p>Delhi University</p>
                            </div>

                            <div className="m-myProfileAdd__info--action">
                                <Link className="mr-15"><i className="db-edit-icon"></i></Link>
                                <Link className="m-db-btn-close"></Link>
                            </div>
                        </div>
                        <p className="m-myProfileAdd__info--duration">
                            <span className="infoItem">Full time</span>  <span className="infoItem">2013 - 2016</span>
                        </p>
                    </div>
                </div>
            </div>

            <div className="m-card">
                <h2>Education</h2>
                <p>By adding your education you will be able to get expert recommendation for your career</p>
                <button className="btn-xs btn-blue-outline ">Add New</button>
            </div>

            <div className="m-card">
                <div className="d-flex justify-content-between mb-10">
                    <h2>Skills</h2>
                    <button className="btn-xs btn-blue-outline" >Add/ Edit</button>
                </div>

                <div className="m-skills-tag">
                    <span>Dashboard</span>
                    <span>JAVA coding</span>
                    <span>React  JS</span>
                </div>
            </div>

            <div className="m-card">
                <h2>Skills</h2>
                <p>You have not added any skiils</p>
                <button className="btn-xs btn-blue-outline ">Add New</button>
            </div>

            <div className="m-card">
                <div className="m-myProfile--heading mb-15 w-100">
                    <h2>Certification</h2>
                    <button className="btn-xs btn-blue-outline ">Add New</button>
                </div>

                <div className="m-myProfileAdd">
                    <span className="m-myProfileAdd--iconCircle m-db-certification"></span>

                    <div className="m-myProfileAdd__info">
                        <div className="m-myProfileAdd__info--heading">
                            <h3>Six Sigma Green Belt Professional</h3>

                            <div className="m-myProfileAdd__info--action">
                                <Link className="mr-15"><i className="db-edit-icon"></i></Link>
                                <Link className="m-db-btn-close"></Link>
                            </div>
                        </div>
                        <p className="m-myProfileAdd__info--duration">
                            <span className="infoItem">By Edureka</span>  <span className="infoItem">Dec. 2014</span>
                        </p>  
                    </div>
                </div>
            </div>

            <div className="m-card">
                <h2>Certification</h2>
                <p>Add certification in your profile to get expert recommendations</p>
                <button className="btn-xs btn-blue-outline ">Add New</button>
            </div>


            
        </div>
    )
}
   
export default MyProfile;