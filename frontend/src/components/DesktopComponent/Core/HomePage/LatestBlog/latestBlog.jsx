import React from 'react';
import './latestBlog.scss';
import { imageUrl } from "utils/domains";
import { useSelector } from 'react-redux';
   
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
                                        <a href={'#'}>
                                            <figure>
                                                <img src={`${imageUrl}desktop/blog-pic1.jpg`} className="img-fluid" alt="Latest from blog" />
                                                <span>Career prospects</span>
                                            </figure>
                                            <strong>Planning required before re- locating to a new city…</strong>
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