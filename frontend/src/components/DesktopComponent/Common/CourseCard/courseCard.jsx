import React from 'react';
import { siteDomain } from 'utils/domains';

const CourseCard = (props) => {
    const { course, name, indx } = props;
    
    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    return (
        <li className="col" key={indx} itemProp="itemListElement" itemScope itemType="https://schema.org/ListItem">
            <div className="card">
                <div className="card__heading">
                    <figure>
                        { course.imgUrl || course.vendor_image && <img itemProp="image" src={course.imgUrl || course.vendor_image} alt={course.imgAlt || course.name || course.heading} /> }
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
                            {name != 'otherProviders' && <span itemProp="ratingValue">{course.rating?.toFixed(1)}/5</span>}
                            {name === 'otherProviders' && course.avg_rating && <span itemProp="ratingValue">{course.avg_rating}/5</span>}
                        </span>
                    </div>
                    <div className="card__price mt-10">
                        <strong>{(course.price || course.inr_price)}/-</strong>
                    </div>
                </div>
            </div>
        </li>
    )
}

export default CourseCard;
