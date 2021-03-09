import React, {useState} from 'react';
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import './Reviews.scss';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const LearnersStories = (props) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <section id="reviews" className="container" data-aos="fade-up">
            <div className="row">
                <h2 className="heading2 m-auto pb-20">Reviews</h2>
                <Carousel className="reviews">
                    <Carousel.Item interval={10000000000}>
                        <div className="d-flex col">
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Abhishek Sinha</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Gaurav Singh</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Shruti Sharma</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="d-flex col">
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Abhishek Sinha</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Gaurav Singh</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Shruti Sharma</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="d-flex col">
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Abhishek Sinha</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Gaurav Singh</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                    </span>
                                    <strong className="card__name">Very useful!!!</strong>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Shruti Sharma</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                        </div>
                    </Carousel.Item>
                </Carousel>
                <div className="d-flex mx-auto mt-20">
                    <Link to={"#"} onClick={handleShow} className="btn btn-outline-primary btn-custom">Write a review</Link>
                </div>
                <Modal show={show} 
                    onHide={handleClose}
                    {...props}
                    // size="md"
                    dialogClassName="write-reviews-box"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    
                    <Modal.Header closeButton>
                    </Modal.Header>
                    <Modal.Body>
                        <h2 className="mb-20">Write a Review</h2>
                        <span className="rating">
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-fullstar-big"></em>
                            <em className="icon-blankstar-big"></em>
                            <span>Click on rate to scale of 1-5</span>
                        </span>
                        <form className="mt-30">
                            <div className="form-group error">
                                <input type="text" className="form-control" id="name" name="name" placeholder=" "
                                    value="" aria-required="true" aria-invalid="true" />
                                <label for="">Title</label>
                                <span class="error-msg">Required</span>
                            </div>
                            <div className="form-group">
                                <textarea className="form-control" rows="3" id="mesage" name="mesage" placeholder=" "
                                    value="" aria-required="true" aria-invalid="true" />
                                <label for="">Review</label>
                            </div>
                            <button type="submit" className="btn btn-inline btn-primary submit-btn mx-auto" role="button">Submit</button>
                        </form>
                    </Modal.Body>
                </Modal>
            </div>
        </section>
    )
}

export default LearnersStories;