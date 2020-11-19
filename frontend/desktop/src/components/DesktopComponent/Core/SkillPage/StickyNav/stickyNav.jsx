import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import { LinkScroll as Link } from 'react-scroll';
import './stickyNav.scss';
import { useSelector} from "react-redux";

const StickyNav = (props) => {

    const { name } = useSelector( store => store.skillBanner )

    return(
        <Navbar className="container-fluid lightblue-bg sticky-nav" expand="lg">
           <div className="container">
                <div className="flex-100">
                    <h2>{name} Courses & Certification</h2>
                    <Nav>
                        <Nav.Link className="active" href="#home">About</Nav.Link>
                        <Nav.Link href="#link">Skills you gain</Nav.Link>
                        <Nav.Link href="#home">Courses</Nav.Link>
                        <Nav.Link href="#home">Why choose us</Nav.Link>
                        <Nav.Link href="#home">FAQs</Nav.Link>
                        <Nav.Link href="#home">Learner’s stories</Nav.Link>
                    </Nav>
                </div>
                <Form inline>
                    <button type="submit" className="btn btn-primary ml-auto" role="button">Submit</button>
                </Form>
            </div> 
        </Navbar>
    )
}

export default StickyNav;