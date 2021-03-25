import React from 'react';
import { siteDomain } from 'utils/domains';

const CourseCard = (props) => {
    const { course, key, name } = props;
    
    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    return (
        <li className="col" key={key}>
            <div className="card">
                <div className="card__heading">
                    <figure>
                        { course.imgUrl && <img src={course.imgUrl || course.vendor_image} alt={course.imgAlt || course.vendor_image} /> }
                    </figure>
                    <h3 className="heading3">
                        <a href={`${siteDomain}${course.url}`}>{course.name || course.heading}</a>
                    </h3>
                </div>
                <div className="card__box">
                    <div className="card__rating">
                        <span className="mr-10">By {(course.providerName || course.vendor)?.split(' ')[0]?.length > 10 ? (course.providerName || course.vendor)?.split(' ')[0]?.slice(0,10) + '...' : (course.providerName || course.vendor)?.split(' ')[0] }</span>

                        <span className="rating">
                            {(course.stars || course.rating)?.map((star, index) => starRatings(star, index))}
                            {name != 'otherProviders' && <span>{course.rating?.toFixed(1)}/5</span>}
                            {name === 'otherProviders' && course.avg_rating && <span>{course.avg_rating}/5</span>}
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
