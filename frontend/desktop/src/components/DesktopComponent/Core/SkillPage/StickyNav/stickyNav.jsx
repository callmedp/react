import React, {useEffect} from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNav.scss';
import { Link as LinkScroll } from "react-scroll";
import { useSelector } from 'react-redux'

const StickyNav = (props) => {
    const [scrolled, setScrolled] = React.useState(false);
    const { name } = useSelector( store => store.skillBanner )

    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 180 ) {
            setScrolled(true);
        }
        else setScrolled(false);
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
    });

    return(
        scrolled ? <Navbar className="container-fluid lightblue-bg sticky-nav sticky-top d-sticky" expand="lg">
           <div className="container">
                <div className="flex-100">
                    <h2>{name} Courses & Certification</h2>
                    <Nav id="content">
                        <LinkScroll to="about" isDynamic={true} spy={true} smooth={true} offset={-120}>
                            <Nav.Link >About</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="skGain" isDynamic={true} spy={true} smooth={true} offset={-80}>
                            <Nav.Link >Skills you gain</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="courses" isDynamic={true} spy={true} smooth={true} offset={-120}>
                            <Nav.Link >Courses</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="choose" isDynamic={true} spy={true} smooth={true} offset={-100}>
                            <Nav.Link >Why choose us</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="faq" isDynamic={true} spy={true} smooth={true} offset={-80}>
                            <Nav.Link >FAQs</Nav.Link>
                        </LinkScroll>
                        
                        <LinkScroll to="story" isDynamic={true} spy={true} smooth={true} offset={-150}>
                            <Nav.Link >Learner’s stories</Nav.Link>
                        </LinkScroll>

                         <LinkScroll to="story1" className="invisible" isDynamic={true} spy={true} smooth={true} offset={0}></LinkScroll>
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