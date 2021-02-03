import React from 'react';
import { Link } from 'react-router-dom';
import { imageUrl, siteDomain } from 'utils/domains';
import '../MyCourses/myCourses.scss';
import '../MyServices/myServices.scss';
   
const EmptyInbox = (props) => {
    const { inboxType, inboxText } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}desktop/no-courses.png`} alt=""/>
                <p className="db-nocourses--text">
                    {inboxText === '' ? 'Seems like no ' + inboxType + ' added to your profile' : inboxText}
                </p>

                <Link to={siteDomain} className="btn btn-outline-primary font-weight-bold">Browse {inboxText === '' ? inboxType : ''}</Link>

                {/* {inboxType === 'courses' ? 'Seems like no ' + inboxType + ' / certification' : inboxType === 'services' ? 'Seems like no ' + inboxType + '<br/> added to your profile'} */}
                
                {/* { inboxType === 'services' ? <a href={resumeShineSiteDomain} className="btn btn-outline-primary font-weight-bold">Browse courses</a> :
                <Link to="/online-courses.html" className="btn btn-outline-primary font-weight-bold">Browse {courses}</Link> } */}
            </div>
        </div>
    )
}
   
export default EmptyInbox;