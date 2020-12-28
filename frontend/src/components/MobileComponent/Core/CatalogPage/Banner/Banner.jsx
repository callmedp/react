import React from 'react';
import { Link } from 'react-router-dom';
import './Banner.scss';

const CatalogBanner = (props) => {
    return (
        <div className="m-container mt-0 mb-10 m-catalog-header">
            <h1 className="m-heading1"><strong>India's largest</strong> e-learning platform</h1>
            <p>Join the club of 4mn learners with our partners like Skillsoft, ACCA etc</p>
            <Link className="btn-white-outline-round mr-10" to={"#"}>View categories</Link>
            <Link className="btn-white-outline-round" to={"#"}>View services</Link>
        </div>
    )
}

export default CatalogBanner;