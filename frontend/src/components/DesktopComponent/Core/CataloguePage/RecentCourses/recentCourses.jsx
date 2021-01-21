import React from 'react';
import './recentCourses.scss';
import { useSelector } from 'react-redux';
import CourseCard from 'components/DesktopComponent/Common/CourseCard/courseCard';

const RecentCourses = (props) => {

    const { recentCoursesList } = useSelector(store => store.recentCourses);

    

    return (
        <section className="container-fluid lightblue-bg mt-30" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="recent-courses mt-40 mb-50">
                        <h2 className="heading2 text-center">Recently added courses</h2>
                        <ul className="recent-courses__list">
                            {
                                recentCoursesList?.slice(0,4).map((course, index) => <CourseCard key={index} course={course} />)
                            }

                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default RecentCourses;