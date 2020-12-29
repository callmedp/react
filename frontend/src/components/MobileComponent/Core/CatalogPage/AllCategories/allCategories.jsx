import React, {useState} from 'react';
import './allCategories.scss';
import { categoryList } from 'utils/constants';

const AllCategories = (props) => {
    return(
        <section id="m-all-categories" className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up" id="categories">
            <div className="m-all-category">
                <h2 className="m-heading2 text-center">All categories</h2>
                <ul className="m-all-category__list">
                    {
                        categoryList?.slice(0,9)?.map(category => {
                            return (
                                <li key={category.id}>
                                    <div className="m-card">
                                        <figure>
                                            <img src={category.mobileImagePath} className="img-fluid" alt={category.name} />
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
        </section>
    )
}
   
export default AllCategories;