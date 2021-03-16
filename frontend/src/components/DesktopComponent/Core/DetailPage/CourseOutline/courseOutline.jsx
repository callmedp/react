import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
// import { Link } from 'react-router-dom';
import './courseOutline.scss'

const CourseOutline = (props) => {
    const {chapter_list} = props;
    console.log(chapter_list);
    return (
        <section id="courseoutline" className="container-fluid mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="faq d-flex course-outline">
                        <div className="course-outline__list">
                            <h2 className="heading2 ml-20 mb-20">Course outline</h2>
                            <Accordion defaultActiveKey="0">
                                {
                                    chapter_list?.map((chap, indx) => {
                                        return (
                                            <Card data-aos="fade-up" key={indx}>
                                                <Accordion.Toggle as={Card.Header} eventKey={chap.ordering}>
                                                <h3>{chap.heading}</h3>
                                                </Accordion.Toggle>
                                                <Accordion.Collapse eventKey={chap.ordering}>
                                                    <Card.Body dangerouslySetInnerHTML={{__html: chap.content}}></Card.Body>
                                                </Accordion.Collapse>
                                            </Card>
                                        )
                                    })
                                }
                                {/* <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="0">
                                    <h3>Introduction to Digital Marketing</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="0">
                                        <Card.Body>
                                            <p>Learning Objectives - In this module, you will learn about different aspects of Digital Marketing and how they come together in a cohesive and effective Digital Marketing plan. </p>
                                            <p>Topics - Introduction to Digital Marketing, The 4-Cs of Digital Marketing, Customer Persona, Comparing digital and offline marketing, Introduction to Google Analytics and Webmaster tools, Introduction to sales funnels. </p>
                                            <p>Handouts Common Ecommerce terminology Customer Persona template</p>
                                        </Card.Body>
                                    </Accordion.Collapse>
                                </Card> */}
                                {/* <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="1">
                                    <h3>How to choose a resume format?</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="1">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="2">
                                    <h3>Why are resume formats important?</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="2">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="3">
                                    <h3>What makes a resume good and attractive?</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="3">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="4">
                                    <h3>Why are resume formats important?</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="4">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="5">
                                    <h3>What makes a resume good and attractive?</h3>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="5">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card> */}
                            </Accordion>
                        </div>
                        <div className="course-outline__img">
                            <img src="/media/images/desktop/course-outline-bg.png" alt="Course outline" />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default CourseOutline;