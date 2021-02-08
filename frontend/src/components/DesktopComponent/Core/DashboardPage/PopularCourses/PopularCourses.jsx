import React from 'react';
import CourseCard from 'components/DesktopComponent/Common/CourseCard/courseCard';
import { useSelector } from 'react-redux';

const PopularCourses = (props) => {

    const { trendingCourses } = useSelector(store => store.footer);

    return (
        <div>
            <section className="container-fluid mt-30">
                <div className="row">
                    <div className="container">
                        <div className="recent-courses mt-40 mb-50">
                            <h2 className="heading2 text-center">Popular Courses</h2>
                            <ul className="recent-courses__list">
                                {
                                    trendingCourses?.slice(0, 4).map((course, index) => <CourseCard key={index} course={course} />)
                                }
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default PopularCourses;