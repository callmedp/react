import React, {useEffect} from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNav.scss';
import { Link as LinkScroll } from "react-scroll";

const StickyNav = (props) => {
    const [scrolled,setScrolled] = React.useState(false);

    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 180 ) {
            setScrolled(true);
        }
        else setScrolled(false);

        // console.log(window)
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
    });

    return(
        scrolled ? <Navbar className="container-fluid lightblue-bg sticky-nav sticky-top d-sticky" expand="lg">
           <div className="container">
                <div className="flex-100">
                    <h2>Digital Marketing Courses & Certification</h2>
                    <Nav>
                        <LinkScroll to="aboutSect" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={-150} duration={800}>
                            <Nav.Link >About</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="skillG" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={-80} duration={800}>
                            <Nav.Link >Skills you gain</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="courseTr" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={-130} duration={800}>
                            <Nav.Link >Courses</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="whyChoose" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={-130} duration={800}>
                            <Nav.Link >Why choose us</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="faqs" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={-80} duration={800}>
                            <Nav.Link >FAQs</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="learnerStr" isDynamic={true} spy={true} smooth={true} hashSpy={false} offset={0} duration={800}>
                            <Nav.Link >Learner’s stories</Nav.Link>
                        </LinkScroll>
                    </Nav>
                </div>
                <Form inline>
                    <button type="submit" className="btn btn-primary ml-auto" role="button">Submit</button>
                </Form>
            </div> 
        </Navbar>
        : ''
    )
}

export default StickyNav;