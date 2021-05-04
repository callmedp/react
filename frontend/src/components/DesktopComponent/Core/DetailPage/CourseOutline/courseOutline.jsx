import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import './courseOutline.scss';
import { imageUrl } from 'utils/domains';

const CourseOutline = (props) => {
    const {chapter_list} = props;

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
                                                <Accordion.Toggle class={!!chap.content ? 'card-header' : 'card-header no-dd'} as={Card.Header} eventKey={indx+1}>
                                                    <h3>{chap.heading}</h3>
                                                </Accordion.Toggle>
                                                {
                                                    !!chap.content &&
                                                        <Accordion.Collapse eventKey={indx+1}>
                                                            <Card.Body dangerouslySetInnerHTML={{__html: chap.content}}></Card.Body>
                                                        </Accordion.Collapse>
                                                }
                                            </Card>
                                        )
                                    })
                                }
                            </Accordion>
                        </div>
                        <div className="course-outline__img">
                            <img src={`${imageUrl}desktop/course-outline-bg.png`} alt="Course outline" />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default CourseOutline;