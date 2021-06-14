import React, {useState} from 'react';
import Carousel from 'react-bootstrap/Carousel';
import './boostedCareers.scss';
import { useSelector } from 'react-redux';
import useLearningTracking from 'services/learningTracking';

const handleTestimonialList = (testimonialList) => testimonialList?.map((testimonial, index) => {
    return (
        <div className="col-sm-6" key={index.toString() + testimonial.userName}>
            <div className="card text-center">
                <span className="card__name">{ testimonial.firstName ?  testimonial.firstName[0].toUpperCase() : ""}{ testimonial.lastName ? testimonial.lastName[0].toUpperCase() : ""}</span>
                <p className="card__txt">{ testimonial.review}</p>
                <strong>{testimonial.firstName} {testimonial.lastName}</strong>
                <span className="card__location">{ testimonial.company ?  testimonial.company : <br />}</span>
            </div>
        </div>
    )
});

const BoostedCareers = () => {
    
    const { testimonialCategory } = useSelector(store => store.testimonials)
    const [key, setKey] = useState(0);
    const sendLearningTracking = useLearningTracking();

    const handleSelect = (selectedIndex, e) => {
        if (e !== undefined) {
            setKey(selectedIndex);

            sendLearningTracking({
                productId: '',
                event: `homepage_boosted_careers_${e.target.offsetParent.className}_clicked`,
                pageTitle:`homepage`,
                sectionPlacement:'boosted_careers',
                eventCategory: `${e.target.offsetParent.className}_${selectedIndex}`,
                eventLabel: e.target.offsetParent.className,
                eventAction: 'click',
                algo: '',
                rank: selectedIndex,
            })
        }
    }

    return (
        <>
            {
                testimonialCategory?.length > 0 && 
                <section className="container" data-aos="fade-up">
                    <div className="row">
                        <div className="container d-flex align-items-center">
                            <div className="col-sm-2">
                                <figure className="icon-quote mb-20"></figure>
                                <h2 className="heading2">See how they boosted their careers</h2>
                            </div>
                            <Carousel className="boosted-careers" activeIndex={key} onSelect={handleSelect}>
                                {
                                    testimonialCategory?.map((testimonialList, idx) => {
                                        return (
                                            <Carousel.Item interval={10000000000} key={idx}>
                                                <div className="d-flex col">
                                                    {
                                                        handleTestimonialList(testimonialList)
                                                    }
                                                </div>
                                            </Carousel.Item>
                                        )
                                    })}
                            </Carousel>
                        </div>
                    </div>
                </section>
            }
        </>
    )
}

export default BoostedCareers;