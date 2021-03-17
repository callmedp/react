import React from 'react';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import { Link } from 'react-router-dom';
   
const OtherProviders = (props) => {
    const {pop_list} = props;
    
    return(
        <section className="container-fluid" data-aos="fade-up" id="popListTemplate">
            <div className="row">
                <div className="container"> 
                    <div className="recent-courses mt-20 mb-30">
                        <h2 className="heading2">Courses by other providers</h2>
                        <ul className="recent-courses__list mt-30">
                            {
                                pop_list?.map((popList, indx) => {
                                    return (
                                        <li className="col" key={indx}>
                                            <div className="card">
                                                <div className="card__heading">
                                                    <figure>
                                                        <img src={popList.vendor_image} />
                                                    </figure>
                                                    <h3 className="heading3">
                                                        <Link to={popList.url ? popList.url : "#"}>{popList.heading}</Link>
                                                    </h3>
                                                </div>
                                                <div className="card__box">
                                                    <div className="card__rating">
                                                        <span className="mr-10">By {popList.vendor}</span>
                                                        <span className="rating">
                                                            <em className="icon-fullstar"></em>
                                                            <em className="icon-fullstar"></em>
                                                            <em className="icon-fullstar"></em>
                                                            <em className="icon-fullstar"></em>
                                                            <em className="icon-blankstar"></em>
                                                            <span>4/5</span>
                                                        </span>
                                                    </div>
                                                    <div className="card__price mt-10">
                                                        <strong>{popList.inr_price}/-</strong> 
                                                    </div>
                                                </div>
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
   
export default OtherProviders;