import React, { useEffect, useState } from 'react';
import { useDispatch, connect } from 'react-redux';
import { siteDomain } from 'utils/domains';
import CustomOverlay from 'services/CustomOverlay';
import PopoverDetail from '../PopOverDetail/popOverDetail'
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo, getTrackingParameters } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const Product = (props) => {

    const { product: {
        name, jobsAvailable,
        providerName, rating, mode,
        price, imgUrl, url,
        tags, about, skillList,
        highlights, type, level,
        brochure, duration,
        u_courses_benefits, u_desc
    },
        index,
        listIdx } = props

    const [halfStar, setHalfStar] = useState(false)

    const tracking_data = getTrackingInfo();

    const trackingParameters = getTrackingParameters(tracking_data);
    const { userTrack, gaTrack } = props;

    useEffect(() => {
        if (!Number.isInteger(rating)) {
            setHalfStar(true)
        }
        else {
            setHalfStar(false)
        }
    }, [rating])

    const handleTracking = () => {
        gaTrack('SkillAllCourses', 'ln_course_click', 'ln_all_' + name, 'ln_' + name,'', false, true);
        userTrack({'query' :tracking_data, 'action' :'exit_skill_page'});
    }

    return (

        <CustomOverlay
            component={<PopoverDetail popoverData={{ about, skillList, highlights, jobsAvailable, url, type, level, u_courses_benefits, u_desc }} />}
            placement={ listIdx === 2  ? 'left' : 'right'}
            onMouseEnter={() => { }}
            delay={200}
        >
            <li className="col-sm-4" key={index} itemProp="itemListElement" itemScope itemType="http://schema.org/ListItem">
                <div className="card" data-aos="fade-zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay={index*50+50} data-aos-duration="1000">
                    <div className="card__heading">
                        {tags === 2 && <span className="flag-blue">NEW</span>}
                        {tags === 1 && <span className="flag-red">BESTSELLER</span>}
                        <figure>
                            <img src={imgUrl} alt={name} itemProp="image" />
                        </figure>
                        <h3 className="heading3">
                            <a itemProp="url" href={`${siteDomain}${url}${trackingParameters}`} onClick={handleTracking} >{name}</a>
                        </h3>
                    </div>
                    <div className="card__box">
                        <div className="card__rating mt-5">
                            <span itemProp="name" className="provider mr-10">By {providerName}</span>
                            <span className="rating">

                                {Array(parseInt(rating)).fill().map((_, index) => <em key={index} className="icon-fullstar"></em>)}
                                {halfStar && <em className="icon-halfstar"></em>}
                                {Array(5 - Math.round(rating)).fill().map((_, index) => <em key={index} className="icon-blankstar"></em>)}

                                <span>{rating}/5</span>
                            </span>
                        </div>
                        <div className="card__duration-mode mt-10">
                            Duration: <strong>{duration} days</strong>  |   Mode: <strong>{mode}</strong>
                        </div>
                        <div className="card__price mt-30">
                            <strong>{price}/-</strong>
                            { brochure ? <a href={brochure} className="icon-pdf" aria-label="pdf icon"></a> : '' }
                        </div>
                    </div>
                </div>
            </li>
        </CustomOverlay>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "userTrack": (data) => {
            return dispatch(trackUser(data))
        },
        "gaTrack": (data) => {
            MyGA.SendEvent(data)
        }
    }
}

export default connect(null, mapDispatchToProps)(Product);
