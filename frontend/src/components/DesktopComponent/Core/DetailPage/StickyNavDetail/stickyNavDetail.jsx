import React from 'react';
import {Link} from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNavDetail.scss';

const StickyNav = (props) => {
    return(
        <Navbar className="container-fluid lightblue-bg sticky-nav-detail" expand="lg">
           <div className="container">
                <div className="flex-1">
                    <span className="d-flex">
                        <figure className="sticky-icon-thumb">
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h2>Digital Marketing Courses & Certification</h2>
                    </span>
                    <Nav>
                        <Nav.Link className="active" href="#keyfeatures">Key Features</Nav.Link>
                        <Nav.Link href="#courseoutline">Course Outline</Nav.Link>
                        <Nav.Link href="#outcome">Outcome</Nav.Link>
                        <Nav.Link href="#howitworks">How it works</Nav.Link>
                        <Nav.Link href="#faqs">FAQs</Nav.Link>
                        <Nav.Link href="#reviews">Reviews</Nav.Link>
                    </Nav>
                </div>
                <Form inline className="course-enrol-sticky">
                    <strong className="mt-20">3,499/- <del>5,499/-</del></strong>
                    <span className="d-flex">
                        <Link to={"#"} className="btn btn-outline-primary">Enquire now</Link>
                        <Link to={"#"} className="btn btn-secondary ml-10">Enroll now</Link>
                    </span>
                </Form>
            </div> 
        </Navbar>
    )
}

export default StickyNav;