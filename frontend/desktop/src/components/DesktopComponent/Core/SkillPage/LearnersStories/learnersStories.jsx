import React from 'react';
import Carousel from 'react-bootstrap/Carousel';
import './learnersStories.scss';
import { useSelector } from 'react-redux';

const LearnersStories = (props) => {


    const { storiesList } = useSelector(store => store.skillBanner)


    return (
        <section className="container" id="learnerStr">
            <div className="row">
                <h2 className="heading2 m-auto pb-20">Learners stories</h2>
                <Carousel className="learner-stories">
                    {
                        storiesList?.map((story, index) => {
                            return (
                                <Carousel.Item key={index}>
                                    <div className="d-flex col">
                                        {
                                            story?.map((item, idx) => {
                                                return (
                                                    <div className="col-sm-4" key={index.toString() + idx.toString() + item.userName}>
                                                        <div className="card text-center">
                                                            <span className="card__name">AS</span>
                                                            <p className="card__txt">{item.review}</p>
                                                            <strong>{item.userName}</strong>
                                                            <span className="card__location">{item.company}</span>
                                                        </div>
                                                    </div>
                                                )
                                            })
                                        }
                                    </div>
                                </Carousel.Item>

                            )
                        })
                    }

                    {/* <Carousel.Item>
                        <div className="d-flex col">
                            <div className="col-sm-4">
                                <div className="card text-center">
                                    <span className="card__name">AS</span>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Abhishek Sinha</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card text-center">
                                    <span className="card__name">GS</span>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Gaurav Singh</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
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
                            <div className="col-sm-4">
                                <div className="card text-center">
                                    <span className="card__name">AS</span>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Abhishek Sinha</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card text-center">
                                    <span className="card__name">GS</span>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Gaurav Singh</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                            <div className="col-sm-4">
                                <div className="card text-center">
                                    <span className="card__name">SS</span>
                                    <p className="card__txt">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.</p>
                                    <strong>Shruti Sharma</strong>
                                    <span className="card__location">Sapient, Noida</span>
                                </div>
                            </div>
                        </div>
                    </Carousel.Item> */}
                </Carousel>
            </div>
        </section>
    )
}

export default LearnersStories;