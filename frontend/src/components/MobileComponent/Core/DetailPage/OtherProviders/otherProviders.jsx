import React from 'react';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import ProductCards from '../ProductCards/productCards';

const OtherProviders = (props) => {
    const { pop_list } = props;
    
    return(
        <section className="m-container mt-0 mb-0 pr-0" id='otherProviders' data-aos="fade-up">
            <h2 className="m-heading2 mb-10 mt-10">Courses by other providers</h2>
            <div className="m-courses m-recent-courses ml-10n">
                {
                    pop_list?.length > 0 && <ProductCards page_section={'other_providers'} productList = {pop_list.slice(0, 12)}/>
                }
            </div>
        </section>
    )
}

export default OtherProviders;