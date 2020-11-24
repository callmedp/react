import React from 'react';
import Carousel from 'react-bootstrap/Carousel';
import './learnersStories.scss';
import { useSelector } from 'react-redux';

const LearnersStories = (props) => {
    const { testimonialCategory } = useSelector(store => store.skillBanner)

    const getStories = (story, index) => {
        return (
            <Carousel.Item key={index}>
                <div className="d-flex col">
                    {
                        story?.map((item, idx) => {
                            return (
                                <div className="col-sm-4" key={index.toString() + idx.toString() + item.userName}>
                                    <div className="card text-center">
                                        <span className="card__name">{item.firstName ? item.firstName[0].toUpperCase() : ""}{item.lastName ? item.lastName[0].toUpperCase() : ""}</span>
                                        <p className="card__txt">{item.review}</p>
                                        <strong>{item.firstName + item.lastName}</strong>
                                        <span className="card__location">{item.company}</span>
                                    </div>
                                </div>
                            )
                        })
                    }
                </div>
            </Carousel.Item>
        )
    }


    return (
        <section className="container" id="story">
            <div className="row">
                <h2 className="heading2 m-auto pb-20">Learners stories</h2>
                <Carousel className="learner-stories">
                    {
                        testimonialCategory?.map(getStories)
                    }
                </Carousel>
            </div>
        </section>
    )
}

export default LearnersStories;