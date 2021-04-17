import React from 'react';
import './otherProviders.scss';
import CourseCard from 'components/DesktopComponent/Common/CourseCard/courseCard';
import Carousel from 'react-bootstrap/Carousel';
import { siteDomain } from 'utils/domains';
   
const OtherProviders = (props) => {
    const {pop_list} = props;

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    const getLikeCourses = (courseData, idx) => {
        return (
            <Carousel.Item interval={10000000000} key={idx}>
                <ul className="recent-courses__list mt-30">
                    {
                        courseData?.map((course, indx) => {
                            return (
                                <li className="col-sm-3" key={indx} itemProp="itemListElement" itemScope itemType="https://schema.org/ListItem">
                                    <div className="card">
                                        <div className="card__heading" itemProp="image">
                                            <figure>
                                                { course.imgUrl || course.vendor_image && <img src={course.imgUrl || course.vendor_image} alt={course.imgAlt || course.name || course.heading} /> }
                                            </figure>
                                            <h3 className="heading3" itemProp="item">
                                                <a href={`${siteDomain}${course.url}`}> <span itemProp="name">{course.name || course.heading}</span></a>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                                <span className="mr-10">By {(course.providerName || course.vendor)?.split(' ')[0]?.length > 10 ? (course.providerName || course.vendor)?.split(' ')[0]?.slice(0,10) + '...' : (course.providerName || course.vendor)?.split(' ')[0] }</span>
                        
                                                <span className="rating" itemProp="aggregateRating" itemScope itemType="https://schema.org/AggregateRating">
                                                    {(course.stars || course.rating)?.map((star, index) => starRatings(star, index))}
                                                    { course.avg_rating && <span itemProp="ratingValue">{course.avg_rating}/5</span> }
                                                </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>{(course.price || course.inr_price)}/-</strong>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            )
                        })
                    }
                </ul>
            </Carousel.Item>
        )
    }

    return(
        // <section className="container-fluid" data-aos="fade-up" id="popListTemplate">
        //     <div className="row">
        //         <div className="container"> 
        //             <div className="recent-courses mt-20 mb-30">
        //                 <h2 className="heading2">Courses by other providers</h2>
        //                     <ul className="recent-courses__list mt-30">
        //                         {
        //                             pop_list?.slice(0,4)?.map((popList, indx) => <CourseCard key={indx} indx={indx} course={popList} name={'otherProviders'} />)
        //                         }
        //                     </ul>
        //             </div>
        //         </div>
        //     </div>
        // </section>

        <section className="container-fluid" data-aos="fade-up" id="popListTemplate">
            <div className="row">
                <div className="container">
                    <div className=" mt-20 mb-30">
                        <h2 className="heading2">Courses by other providers</h2>
                        <Carousel className="other-providers">
                            {
                                pop_list?.map(getLikeCourses)
                            }
                        </Carousel>
                        {/* <span className="pink-circle2" data-aos="fade-right"></span>
                        <span className="pink-circle3" data-aos="fade-left"></span> */}
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default OtherProviders;