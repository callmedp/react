import React from 'react';
import './allCategories.scss';
import { useSelector } from 'react-redux';


const AllCategories = () => {

    const { categoryList } = useSelector( store => store.allCategories )

    return (
        <section id="all-categories" className="container-fluid lightblue-bg mt-30" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="all-category mt-40 mb-30">
                        <h2 className="heading2 text-center">All categories</h2>
                        <ul className="all-category__list">
                            {
                                categoryList.map(category => {
                                    return (
                                        <li className="col-sm-3" key={category.url}>
                                            <div className="card">
                                                <figure>
                                                    <img src={category.icon_image} className="img-fluid" alt={category.name} />
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