import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import '../../SkillPage/FAQ/faq.scss';

const FAQ = (props) => {
    return (
        <section className="container-fluid lightgrey-bg mt-40">
            <div className="row">
                <div className="container">
                    <h2 className="heading2 mt-40 text-center">Frequently Asked Questions</h2>
                    <div className="faq d-flex col-10 m-auto">
                        <div className="faq__list">
                            <Accordion defaultActiveKey="0">
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="0">
                                    <strong>How do I earn loyalty points?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="0">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="1">
                                    <strong>How can I redeem loyalty points?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="1">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="2">
                                    <strong>Validity of loyalty points?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="2">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="3">
                                    <strong>Can loyalty points be used for refund?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="3">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="4">
                                    <strong>Will loyalty points be valid on shine.com as well?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="4">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card data-aos="fade-up">
                                    <Accordion.Toggle as={Card.Header} eventKey="5">
                                    <strong>Can I buy third party stuff from loyalty points?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="5">
                                    <Card.Body>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                            </Accordion>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FAQ;