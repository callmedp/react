import React from 'react';
import Carousel from 'react-bootstrap/Carousel';
import './learnersStories.scss';
import { useSelector } from 'react-redux';


const getStories = (story, index) => {
    return (
        <Carousel.Item interval="1000000" key={index}>
            <div className="d-flex col">
                {
                    story?.map((item, idx) => {
                        return (
                            <div className="col-sm-4" key={index.toString() + idx.toString() + item.userName}>
                                <div className="card text-center">
                                    <span itemprop="name" className="card__name" itemprop="name">{item.firstName ? item.firstName[0].toUpperCase() : ""}{item.lastName ? item.lastName[0].toUpperCase() : ""}</span>
                                    <p className="card__txt" itemprop="description">{item.review}</p>
                                    <strong itemprop="author">{item.firstName + item.lastName}</strong>
                                    <span className="card__location">{item.company ? item.company : <br />}</span>
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        </Carousel.Item>
    )
}


const LearnersStories = (props) => {
    const { testimonialCategory } = useSelector(store => store.skillBanner)


    return (
        testimonialCategory.length ? (
            <section className="container" id="story" data-aos="fade-up" itemscope itemtype="http://schema.org/UserReview">
                <div className="row">
                    <h2 className="heading2 m-auto pb-20">Learners stories</h2>
                    <Carousel className="learner-stories">
                        {
                            testimonialCategory?.map(getStories)
                        }
                    </Carousel>
                </div>
            </section>
        ) : null
    )
}

export default LearnersStories; 