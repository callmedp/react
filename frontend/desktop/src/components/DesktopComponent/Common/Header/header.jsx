import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss';

const Header = (props) => {
    const showTab = () =>{
        console.log(this)
        
    }
    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                    <Link className="navbar-brand" to={"#"}></Link>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <form className="form-inline top-search my-2 my-lg-0 ml-auto">
                            <input className="form-control top-input" type="search" placeholder="Search anything" aria-label="Search" />
                            <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
                        </form>
                        <ul className="navbar-nav navbar-right">
                        <li className="nav-item">
                            <Link className="nav-link" to={"#"}>Practice test</Link>
                        </li>
                        <li className="nav-item dropdown dropdown-jobs">
                            <Link className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Job assistance</Link>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                            <Link className="dropdown-item" to={"#"}>Resume Writing</Link>
                            <Link className="dropdown-item" to={"#"}>International Resume</Link>
                            <Link className="dropdown-item" to={"#"}>Visual Resume</Link>
                            <Link className="dropdown-item" to={"#"}>Jobs On The Move</Link>
                            <Link className="dropdown-item" to={"#"}>Linkedin Profile</Link>
                            <Link className="dropdown-item" to={"#"}>Featured Profile</Link>
                            <Link className="dropdown-item" to={"#"}>Background Verification Services</Link>
                            <Link className="dropdown-item" to={"#"}>Interview Preparation</Link>
                            <Link className="dropdown-item" to={"#"}>Application Highlighter</Link>
                            </div>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to={"#"}>Practice test</Link>
                        </li>
                        <li className="nav-item dropdown dropdown-resources">
                            <Link className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Free resources</Link>
                            <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                            <div className="resources-tab">
                                <ul className="nav nav-tabs" id="myTab" role="tablist" >
                                    <li className="nav-item">
                                        <Link className="nav-link active" id="resources-tab" data-toggle="tab" href="#tab-links1" role="tab" aria-controls="resources-tab" aria-selected="true">Resume Formats</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" id="resources-tab" data-toggle="tab" href="#resources-links2" role="tab" aria-controls="resources-tab" aria-selected="false">Resignation Letter Formats</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" id="resources-tab" data-toggle="tab" href="#resources-links3" role="tab" aria-controls="resources-tab" aria-selected="false">Cover Letter Formats</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" id="resources-tab" data-toggle="tab" href="#resources-links4" role="tab" aria-controls="resources-tab" aria-selected="false">Resume Templates</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" id="resources-tab" data-toggle="tab" href="#resources-links5" role="tab" aria-controls="resources-tab" aria-selected="false">Linkedin Summary Example</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" id="resources-tab" data-toggle="tab" href="#resources-links6" role="tab" aria-controls="resources-tab" aria-selected="false">Career Guidance</Link>
                                    </li>
                                </ul>
                                <div className="tab-content" id="myTabContent">
                                    <div className="tab-pane fade show active" id="resources-links1" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="resources-links2" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="resources-links3" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="resources-links4" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="resources-links5" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="resources-links6" role="tabpanel" aria-labelledby="resources-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to={"#"}>Blog</Link>
                        </li>
                        <li className="nav-item dropdown dropdown-call">
                            <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <figure className="icon-call"></figure>
                            </Link>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                <Link className="dropdown-item" to={"#"}><strong>Call us:</strong> 0124-4312500/01</Link>
                            </div>
                            </li>
                            <li className="nav-item dropdown dropdown-user">
                                <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <figure className="icon-user"></figure>
                                </Link>
                                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                <Link className="dropdown-item" to={"#"}>My Inbox</Link>
                                <Link className="dropdown-item" to={"#"}>My Orders</Link>
                                <Link className="dropdown-item" to={"#"}>My Wallet</Link>
                                <Link className="dropdown-item" to={"#"}>My Referrals</Link>
                                <Link className="dropdown-item" to={"#"}>abc@hindustantimes.com</Link>
                                <div className="dropdown-divider"></div>
                                <Link className="dropdown-item" to={"#"}>Logout</Link>
                                </div>
                            </li>
                            <li className="nav-item position-relative">
                                <span className="counter">4</span>
                                <Link className="nav-link link-ht" to={"#"}>
                                    <figure className="icon-cart"></figure>
                                </Link>
                            </li>
                        </ul>
                        
                    </div>
                    </div>
                </div>
            </nav>

            <nav className="navbar-bg-light navbar navbar-expand-lg navbar-light">
                <div className="container">
                    <div className="row">
                    <ul className="navbar-nav" id="categories">
                        <li className="nav-item dropdown dropdown-categories">
                            <Link className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <span className="sm-txt">Explore</span>Categories
                            <figure className="icon-down"></figure>
                            </Link>
                            <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                            <div className="categories-tab">
                                <ul className="nav nav-tabs" id="myTab" role="tablist" onMouseEnter={()=>showTab()}>
                                    <li className="nav-item" role="presentation" >
                                        <Link className="nav-link active" id="category-tab" data-toggle="tab" href="#tab-links1" role="tab" aria-controls="category-tab" aria-selected="true">Sales & Marketing</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links2" role="tab" aria-controls="category-tab" aria-selected="false">Operation Management</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links3" role="tab" aria-controls="category-tab" aria-selected="false">Banking & Finance</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links4" role="tab" aria-controls="category-tab" aria-selected="false">Information Technology</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links5" role="tab" aria-controls="category-tab" aria-selected="false">Human Resources</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links6" role="tab" aria-controls="category-tab" aria-selected="false">Management</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links7" role="tab" aria-controls="category-tab" aria-selected="false">Mass Communication</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links8" role="tab" aria-controls="category-tab" aria-selected="false">Personal Development</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links9" role="tab" aria-controls="category-tab" aria-selected="false">Law</Link>
                                    </li>
                                    <li className="nav-item" role="presentation">
                                        <Link className="nav-link" id="category-tab" data-toggle="tab" href="#tab-links10" role="tab" aria-controls="category-tab" aria-selected="false">Course Catalogue</Link>
                                    </li>
                                </ul>
                                <div className="tab-content" id="myTabContent">
                                    <div className="tab-pane fade show active" id="tab-links1" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links2" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links3" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links4" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links5" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links6" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links7" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links8" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links9" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                    <div className="tab-pane fade" id="tab-links10" role="tabpanel" aria-labelledby="category-tab">
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>Finanacial Reporting and Management</Link>
                                        <Link to={"#"}>Commercial Operation</Link>
                                        <Link to={"#"}>Investment Banking</Link>
                                        <Link to={"#"}>GST</Link>
                                        <Link to={"#"}>Advanced Accounting</Link>
                                        <Link to={"#"}>Banking</Link>
                                        <Link to={"#"}>Risk Management</Link>
                                        <Link to={"#"}>Stock Market Training</Link>
                                        <Link to={"#"}>View all</Link>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>Digital Marketing</Link>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>Six Sigma</Link>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>Project Management</Link>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>Big Data</Link>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>IT Software</Link>
                        </li>
                        <li className="nav-item">
                        <Link className="nav-link" to={"#"}>General Management</Link>
                        </li>
                    </ul>
                    </div>
                </div>
            </nav>
        </div>
    )
} 

export default Header;