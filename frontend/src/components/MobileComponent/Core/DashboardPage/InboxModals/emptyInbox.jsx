import React from 'react';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain, imageUrl } from 'utils/domains';
import '../MyCourses/myCourses.scss';
   
const EmptyInbox = (props) => {

    const { inboxType } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}desktop/no-courses.png`} alt=""/>
                <p className="db-nocourses--text">Seems like no {inboxType === 'courses' ? 'courses / certification' : 'services'}<br/>added to your profile</p>
                { inboxType === 'services' ? <a href={resumeShineSiteDomain} className="btn btn-outline-primary font-weight-bold">Browse courses</a> :
                    <Link to="/online-courses.html" className="btn btn-outline-primary font-weight-bold">Browse courses</Link> }
            </div>
        </div>
    )
}
   
export default EmptyInbox;