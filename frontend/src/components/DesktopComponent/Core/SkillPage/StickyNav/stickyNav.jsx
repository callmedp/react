import React, { useEffect } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import { Nav, Form } from 'react-bootstrap';
import './stickyNav.scss';
import { Link as LinkScroll } from "react-scroll";
import { useSelector } from 'react-redux'

const StickyNav = (props) => {
    const [scrolled, setScrolled] = React.useState(false);
    const { name } = useSelector(store => store.skillBanner)
    const { hasFaq, hasLearnerStories } = props

    const handleScroll = () => {
        const offset = window.scrollY;
        if (offset > 180) {
            setScrolled(true);
        }
        else setScrolled(false);
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
    });

    return (
        scrolled ? <Navbar className="container-fluid lightblue-bg sticky-nav sticky-top d-sticky" expand="lg" data-aos="fade-down" data-aos-duration="500">
            <div className="container">
                <div className="flex-1">
                    <h2>{name} Courses & Certification</h2>
                    <Nav id="content">
                        <LinkScroll to="about" isDynamic={true} spy={true} offset={-120}>
                            <Nav.Link >About</Nav.Link>
                        </LinkScroll>

                        <LinkScroll to="skGain" isDynamic={true} spy={true} offset={-80}>
                            <Nav.Link >Skills you gain</Nav.Link>
                        </LinkScroll>

                        <LinkScroll to="courses" isDynamic={true} spy={true} offset={-120}>
                            <Nav.Link >Courses</Nav.Link>
                        </LinkScroll>

                        <LinkScroll to="choose" isDynamic={true} spy={true} offset={-100}>
                            <Nav.Link >Why choose us</Nav.Link>
                        </LinkScroll>

                        {
                            hasFaq ? <LinkScroll to="faq" isDynamic={true} spy={true} offset={-80}>
                                <Nav.Link >FAQs</Nav.Link>
                            </LinkScroll> : ''
                        }

                        {
                            hasLearnerStories ? <LinkScroll to="story" isDynamic={true} spy={true} offset={-130}>
                                <Nav.Link >Learner’s stories</Nav.Link>
                            </LinkScroll> : ''
                        }


                        <LinkScroll to="story1" className="invisible" isDynamic={true} spy={true} offset={0}></LinkScroll>
                    </Nav>
                </div>
                <LinkScroll to="help" isDynamic={true} spy={true} offset={-80}>
                    <button type="submit" className="btn btn-primary ml-auto sticky-btn" role="button">Need Help?</button>
                </LinkScroll>
            </div>
        </Navbar>
            : ''
    )
}

export default StickyNav;