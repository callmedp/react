import React from 'react';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
// import { Link } from 'react-router-dom';
import CourseCard from 'components/DesktopComponent/Common/CourseCard/courseCard';
   
const OtherProviders = (props) => {
    const {pop_list} = props;

    return(
        <section className="container-fluid" data-aos="fade-up" id="popListTemplate">
        <div className="row">
            <div className="container"> 
                <div className="recent-courses mt-20 mb-30">
                    <h2 className="heading2">Courses by other providers</h2>
                        <ul className="recent-courses__list mt-30">
                            {
                                pop_list?.slice(0,4).map((popList, indx) => <CourseCard key={indx} indx={indx} course={popList} name={'otherProviders'} />)
                            }
                        </ul>
                </div>
            </div>
        </div>
    </section>
    )
}
   
export default OtherProviders;