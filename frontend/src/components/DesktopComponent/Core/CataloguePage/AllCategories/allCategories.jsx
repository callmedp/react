import React from 'react';
import './allCategories.scss';
import { categoryList } from 'utils/constants';



const AllCategories = () => {

    return (
        <section id="all-categories" className="container-fluid lightblue-bg mt-30" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="all-category mt-40 mb-30">
                        <h2 className="heading2 text-center">All categories</h2>
                        <ul className="all-category__list">
                            {
                                categoryList?.slice(0, 9).map(category => {
                                    return (
                                        <li className="col-sm-4" key={category.id}>
                                            <div className="card">
                                                <figure>
                                                    <img src={category.desktopImagePath} className="img-fluid" alt={category.name} />
                                                </figure>
                                                <h3>{category.name}</h3>
                                                <a href={category.url}>View courses</a>
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

export default AllCategories;