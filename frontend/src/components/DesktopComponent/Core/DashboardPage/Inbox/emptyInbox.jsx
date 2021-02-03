import React from 'react';
import { Link } from 'react-router-dom';
import { imageUrl, siteDomain } from 'utils/domains';
import '../MyCourses/myCourses.scss';
import '../MyServices/myServices.scss';
   
const EmptyInbox = (props) => {
    const { inboxButton, inboxText } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}desktop/no-courses.png`} alt="Empty Dashboard Image"/>
                <p className="db-nocourses--text">{inboxText}</p>
                <Link to={siteDomain} className="btn btn-outline-primary font-weight-bold">{inboxButton}</Link>
            </div>
        </div>
    )
}
   
export default EmptyInbox;