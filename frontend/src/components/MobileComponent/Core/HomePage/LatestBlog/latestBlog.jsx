import React from 'react';
import { useSelector } from 'react-redux';
import './latestBlog.scss';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
   
const LatestBlog = (props) => {
    const { latestBlog } = useSelector(store => store.jobAssistance)

    return(
        <section className="m-container mt-0 mb-0 pl-0 pr-0" data-aos="fade-up">
            <div className="m-latest-blog">
                <h2 className="m-heading2-home mb-5 text-center">Latest from blog</h2>
                <ul className="m-latest-blog__list">
                    {
                        latestBlog?.slice(0, 2)?.map((blog, index) => {
                            return (
                                <li className="col pl-0" key={ index }>
                                    <div className="m-card">
                                        <Link to={`${siteDomain}${blog?.url}`}>
                                            <figure>
                                                <img src={blog?.image} className="img-fluid" alt={blog?.display_name} />
                                                <span>{ blog?.p_category?.length > 13 ? blog?.p_category?.slice(0, 13) + '...' : blog?.p_category }</span>
                                            </figure>
                                            <strong>{ blog?.display_name?.length > 40 ? blog?.display_name?.slice(0, 40) + '...' : blog?.display_name }</strong>
                                        </Link>
                                    </div>
                                </li>
                            )
                        })
                    }
                    {/* <li className="col">
                        <div className="m-card">
                            <Link to={"#"}>
                                <figure>
                                    <img src="/media/images/blog-pic1.jpg" className="img-fluid" alt="Latest from blog" />
                                    <span>Career prospects</span>
                                </figure>
                                <strong>Planning required before re- locating to a new city…</strong>
                            </Link>
                        </div>
                    </li>
                    <li className="col pl-0">
                        <div className="m-card">
                            <Link to={"#"}>
                                <figure>
                                    <img src="/media/images/blog-pic2.jpg" className="img-fluid" alt="Latest from blog" />
                                    <span>Career prospects</span>
                                </figure>
                                <strong>Careers that can be opt by learning Autocad</strong>
                            </Link>
                        </div>
                    </li> */}
                </ul>
            </div>
        </section>
    )
}
   
export default LatestBlog;