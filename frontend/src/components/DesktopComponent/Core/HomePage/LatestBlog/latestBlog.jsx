import React from 'react';
import './latestBlog.scss';
// import { imageUrl } from "utils/domains";
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';

const LatestBlog = (props) => {

    const { latestBlog } = useSelector( store => store.jobAssistance )

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
                                    <div className="card">
                                        <a href={`${siteDomain}${blog?.url}`}>
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
                </div>
            </div>
        </section>
    )
}
   
export default LatestBlog;