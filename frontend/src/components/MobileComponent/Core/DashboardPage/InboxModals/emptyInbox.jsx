import React from 'react';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain, imageUrl, siteDomain } from 'utils/domains';
import '../MyCourses/myCourses.scss';
   
const EmptyInbox = (props) => {

    const { inboxType } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}mobile/no-courses.png`} alt=""/>
                <p className="db-nocourses--text">Seems like no {inboxType === 'courses' ? 'courses / certification' : inboxType === 'services' ? 'services' : inboxType === 'orders' ? 'Order' : inboxType === 'wallet' ? 'loyality points' : ''}<br/>added to your profile</p>
                { 
                    inboxType === 'services' ? <a href={resumeShineSiteDomain} className="btn btn-outline-primary font-weight-bold">Browse Services</a> :
                        inboxType === 'courses' ? <Link to="/online-courses.html" className="btn btn-outline-primary font-weight-bold">Browse Courses</Link> :
                            <a href={siteDomain} className="btn btn-outline-primary font-weight-bold">Go to Home</a>  
                }
            </div>
        </div>
    )
}
   
export default EmptyInbox;