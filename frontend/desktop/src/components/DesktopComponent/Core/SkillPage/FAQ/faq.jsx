import React, { useState } from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import './faq.scss'
import { useSelector } from 'react-redux';

const FAQ = (props) => {

    const { faqList } = useSelector(store => store.skillBanner)
    const [sliceFlag, setSliceFlag] = useState(true)

    const loadMore = () => {
        setSliceFlag(state => !state)
    }

    return (
        <section className="container-fluid lightblue-bg mt-40">
            <div className="row">
                <div className="container">
                    <h2 className="heading2 mt-40">Frequently Asked Questions</h2>
                    <div className="faq d-flex">
                        <div className="faq__list">
                            <Accordion defaultActiveKey="0">
                                {
                                    (sliceFlag ? faqList.slice(0, 4) : faqList).map((item, index) => {
                                        return (
                                            <Card key={index}>
                                                <Accordion.Toggle as={Card.Header} eventKey="0">
                                                    <strong>{item.heading}</strong>
                                                </Accordion.Toggle>
                                                <Accordion.Collapse eventKey="0">
                                                    <Card.Body dangerouslySetInnerHTML={{ __html: item.content }}>
                                                    </Card.Body>
                                                </Accordion.Collapse>
                                            </Card>
                                        )
                                    })
                                }
                                {/* <Card>
                                    <Accordion.Toggle as={Card.Header} eventKey="1">
                                    <strong>How to choose a resume format?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="1">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card>
                                    <Accordion.Toggle as={Card.Header} eventKey="2">
                                    <strong>Why are resume formats important?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="2">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card>
                                    <Accordion.Toggle as={Card.Header} eventKey="3">
                                    <strong>What makes a resume good and attractive?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="3">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card>
                                    <Accordion.Toggle as={Card.Header} eventKey="4">
                                    <strong>Why are resume formats important?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="4">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                                <Card>
                                    <Accordion.Toggle as={Card.Header} eventKey="5">
                                    <strong>What makes a resume good and attractive?</strong>
                                    </Accordion.Toggle>
                                    <Accordion.Collapse eventKey="5">
                                    <Card.Body>A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</Card.Body>
                                    </Accordion.Collapse>
                                </Card> */}
                            </Accordion>
                            { sliceFlag ? <Link onClick={loadMore} to={"#"} className="load-more pt-20">Load More FAQS</Link> : '' }
                        </div>
                        <div className="faq__img">
                            <img src="/media/images/faq.svg" alt="Frequently Asked Questions" />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FAQ;