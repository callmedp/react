import React, {useState} from 'react';
import './latestBlog.scss';
import { Link } from 'react-router-dom';

   
const LatestBlog = (props) => {
    return(
        <section className="container-fluid mt-0 mb-0" data-aos="fade-up">
            <div className="row">
                <div className="container"> 
                    <div className="latest-blog mt-40">
                        <h2 className="heading2 mb-5 text-center">Latest from blog</h2>
                        <ul className="latest-blog__list">
                            <li className="col-sm-4">
                                <div className="card">
                                    <Link to={"#"}>
                                        <figure>
                                            <img src="./media/images/blog-pic1.jpg" className="img-fluid" alt="Latest from blog" />
                                            <span>Career prospects</span>
                                        </figure>
                                        <strong>Planning required before re- locating to a new city…</strong>
                                    </Link>
                                </div>
                            </li>
                            <li className="col-sm-4">
                                <div className="card">
                                    <Link to={"#"}>
                                        <figure>
                                            <img src="./media/images/blog-pic2.jpg" className="img-fluid" alt="Latest from blog" />
                                            <span>Career prospects</span>
                                        </figure>
                                        <strong>Careers that can be opt by learning Autocad</strong>
                                    </Link>
                                </div>
                            </li>
                            <li className="col-sm-4">
                                <div className="card">
                                    <Link to={"#"}>
                                        <figure>
                                            <img src="./media/images/blog-pic3.jpg" className="img-fluid" alt="Latest from blog" />
                                            <span>Career prospects</span>
                                        </figure>
                                        <strong>Top 12 Machine Learning Interview Question & Answers 2019</strong>
                                    </Link>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default LatestBlog;