import React from 'react';
import { useSelector } from 'react-redux';
import './latestBlog.scss';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';
import { MyGA } from 'utils/ga.tracking.js';

const LatestBlog = () => {
    const { latestBlog } = useSelector(store => store.jobAssistance)
    const sendLearningTracking = useLearningTracking();

    const latesBlogTracking = (name, category, indx) => {
        let name_scored = name.replace(/ /g, '_');

        MyGA.SendEvent('ln_new_homepage','ln_homepage_blog', 'ln_blog_click', name_scored, '', false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_latest_blog_${category}_${name_scored}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'latest_blog',
            eventCategory: name_scored,
            eventLabel: `${category}_${name_scored}`,
            eventAction: 'click',
            algo: '',
            rank: indx,
        })

    }

    return(
        <section className="m-container mt-0 mb-0 pb-0 pr-0" data-aos="fade-up">
            <div className="m-latest-blog">
                <h2 className="m-heading2-home mb-5 text-center">Latest from blog</h2>
                <ul className="m-latest-blog__list">
                    {
                        latestBlog?.slice(0, 2)?.map((blog, index) => {
                            return (
                                <li className="col pl-0" key={ index }>
                                    <div className="m-card">
                                        <a href={`${siteDomain}${blog?.url}`} onClick={() => latesBlogTracking(blog.display_name, blog?.p_category, index)}>
                                            <figure>
                                                <img src={blog?.image} className="img-fluid" alt={blog?.display_name} />
                                                <span>{ blog?.p_category?.length > 13 ? blog?.p_category?.slice(0, 13) + '...' : blog?.p_category }</span>
                                            </figure>
                                            <strong>{ blog?.display_name?.length > 40 ? blog?.display_name?.slice(0, 40) + '...' : blog?.display_name }</strong>
                                        </a>
                                    </div>
                                </li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}
   
export default LatestBlog;