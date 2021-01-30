import React, {useState} from 'react';
import './latestBlog.scss';
import { Link } from 'react-router-dom';

   
const LatestBlog = (props) => {
    return(
        <section className="m-container mt-0 mb-0 pl-0 pr-0" data-aos="fade-up">
            <div className="m-latest-blog">
                <h2 className="m-heading2-home mb-5 text-center">Latest from blog</h2>
                <ul className="m-latest-blog__list">
                    <li className="col">
                        <div className="m-card">
                            <Link to={"#"}>
                                <figure>
                                    <img src="./media/images/blog-pic1.jpg" className="img-fluid" alt="Latest from blog" />
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
                                    <img src="./media/images/blog-pic2.jpg" className="img-fluid" alt="Latest from blog" />
                                    <span>Career prospects</span>
                                </figure>
                                <strong>Careers that can be opt by learning Autocad</strong>
                            </Link>
                        </div>
                    </li>
                </ul>
            </div>
        </section>
    )
}
   
export default LatestBlog;