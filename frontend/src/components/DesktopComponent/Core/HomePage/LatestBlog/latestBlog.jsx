import React from 'react';
import './latestBlog.scss';
 import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const LatestBlog = () => {
    
    const { latestBlog } = useSelector( store => store.jobAssistance );
    const sendLearningTracking = useLearningTracking();

    const latesBlogTracking = (name, category, url, indx) => {

        MyGA.SendEvent('ln_new_homepage','ln_homepage_blog', 'ln_blog_click', stringReplace(name), '', false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_latest_blog_${category}_${stringReplace(name)}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'latest_blog',
            eventCategory: stringReplace(name),
            eventLabel: `${category}_${stringReplace(name)}`,
            eventAction: 'click',
            algo: '',
            rank: indx,
        })

        window.location.href = `${siteDomain}${url}`;
    }

    return(
        <section className="container-fluid mt-0 mb-0" data-aos="fade-up">
            <div className="row">
                <div className="container"> 
                    <div className="latest-blog mt-40">
                        <h2 className="heading2 mb-5 text-center">Latest from blog</h2>
                        <ul className="latest-blog__list">
                          { 
                            latestBlog?.map((blog, idx) => {
                                return (
                                    <li className="col-sm-4" key={idx}>
                                        <div className="card cursorLink" onClick={() => latesBlogTracking(blog.display_name, blog?.p_category, blog?.url, idx)}>
                                            <figure>
                                                <img src={blog?.image} className="img-fluid" alt={blog?.display_name} />
                                                <span>{ blog?.p_category?.length > 13 ? blog?.p_category?.slice(0, 13) + '...' : blog?.p_category }</span>
                                            </figure>
                                            <strong>{ blog?.display_name?.length > 40 ? blog?.display_name?.slice(0, 40) + '...' : blog?.display_name }</strong>
                                        </div>
                                    </li>
                                )
                            })
                          }
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default LatestBlog;