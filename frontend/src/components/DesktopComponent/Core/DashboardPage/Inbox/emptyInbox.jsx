import React from 'react';
import { Link } from 'react-router-dom';
import { imageUrl, siteDomain } from 'utils/domains';
import '../MyCourses/myCourses.scss';
import '../MyServices/myServices.scss';
   
const EmptyInbox = (props) => {
    const { inboxButton, inboxText, redirectUrl } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src={`${imageUrl}desktop/no-courses.png`} alt="Empty Dashboard Image"/>
                <p className="db-nocourses--text">{inboxText}</p>
                <a href={redirectUrl} className="btn btn-outline-primary font-weight-bold">{inboxButton}</a>
            </div>
        </div>
    )
}
   
export default EmptyInbox;