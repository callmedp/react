import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import { LinkScroll as Link } from 'react-scroll';
import './stickyNav.scss';
import { useSelector} from "react-redux";

const StickyNav = (props) => {

    const { name } = useSelector( store => store.skillBanner )
   

    const scroll = () =>    {
        // window.scrollTo({
        //     top: 100,
        //     behavior: 'smooth'
        //   });
        //   console.log("top", storyRef, chooseRef, gainRef)
        // console.log("props",props.allRef)
    }

    return(
        <Navbar className="container-fluid lightblue-bg sticky-nav" expand="lg">
           <div className="container">
                <div className="flex-100">
                    <h2>{name} Courses & Certification</h2>
                    <Nav>
                        <Nav.Link onSelect={scroll} href="#about" className="active" >About</Nav.Link>
                        <Nav.Link href="#gain" >Skills you gain</Nav.Link>
                        <Nav.Link href="#courses" >Courses</Nav.Link>
                        <Nav.Link href="#choose" >Why choose us</Nav.Link>
                        <Nav.Link href="#faq" >FAQs</Nav.Link>
                        <Nav.Link href="#story" >Learner’s stories</Nav.Link>
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