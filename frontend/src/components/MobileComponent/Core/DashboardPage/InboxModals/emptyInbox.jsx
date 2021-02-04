import React from 'react';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain, imageUrl, siteDomain } from 'utils/domains';
import '../MyCourses/myCourses.scss';
   
const EmptyInbox = (props) => {

    const { inboxType } = props;

    const serviceMessage = 'There is no service added to your profile!'
    const courseMesaage = 'Seems like no courses / certification added to your profile!'
    const orderMessage = 'You have not ordered any product till now!'
    const walletMessage = 'Your wallet is empty!'

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}mobile/no-courses.png`} alt=""/>
                <p className="db-nocourses--text">{inboxType === 'courses' ? courseMesaage : inboxType === 'services' ? serviceMessage : inboxType === 'orders' ? orderMessage : inboxType === 'wallet' ? walletMessage : ''}</p>
                { 
                    inboxType === 'services' ? <a href={resumeShineSiteDomain} className="btn btn-outline-primary font-weight-bold">Go to Home</a> :
                        inboxType === 'courses' ? <Link to="/online-courses.html" className="btn btn-outline-primary font-weight-bold">Browse Courses</Link> :
                            <a href={siteDomain} className="btn btn-outline-primary font-weight-bold">Go to Home</a>  
                }
            </div>
        </div>
    )
}
   
export default EmptyInbox;