import React from 'react';
import Carousel from 'react-bootstrap/Carousel';
import './boostedCareers.scss';

const BoostedCareers = (props) => {
    return (
        <section className="container" data-aos="fade-up">
            <div className="row">
                <div className="container d-flex align-items-center">
                    <div className="col-sm-2">
                        <h2 className="heading2">See how they boosted their careers</h2>
                    </div>
                    <Carousel className="boosted-careers">
                        <Carousel.Item interval={10000000000}>
                            <div className="d-flex col">
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">AS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Abhishek Sinha</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">GS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Gaurav Singh</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                            </div>
                        </Carousel.Item>
                        <Carousel.Item>
                            <div className="d-flex col">
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">GS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Gaurav Singh</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">SS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Shruti Sharma</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                            </div>
                        </Carousel.Item>
                        <Carousel.Item>
                            <div className="d-flex col">
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">AS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Abhishek Sinha</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="card text-center">
                                        <span className="card__name">GS</span>
                                        <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                        <strong>Gaurav Singh</strong>
                                        <span className="card__location">Sapient, Noida</span>
                                    </div>
                                </div>
                            </div>
                        </Carousel.Item>
                    </Carousel>
                </div>
            </div>
        </section>
    )
}

export default BoostedCareers;