import React from 'react';
import { Link } from 'react-router-dom';
import './myCourses.scss'

   
const MyCourses = (props) => {

    const { inboxType } = props;

    return(
        <div>
            <div className="db-nocourses">
                <img src="/media/images/no-courses.png" alt=""/>
                <p className="db-nocourses--text">Seems like no {inboxType === 'courses' ? 'courses / certification' : 'services'}<br/>added to your profile</p>
                <Link to={"#"} className="btn btn-outline-primary font-weight-bold">Browse { inboxType === 'courses' ? 'courses' : 'services' }</Link>
            </div>
        </div>
    )
}
   
export default MyCourses;