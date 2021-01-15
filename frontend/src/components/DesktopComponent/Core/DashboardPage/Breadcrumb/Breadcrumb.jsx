import React from 'react';
import { Breadcrumb } from 'react-bootstrap';
import './breadcrumb.scss';

   
const BreadCrumbs = (props) => {
    return(
        <div className="d-flex align-items-center justify-content-between">

            <nav aria-label="breadcrumb">
                <ol className="db-breadcrumb">
                    <li className="db-breadcrumb-item"><a href="#" role="button">Home</a></li>
                    <li className="db-breadcrumb-item active" aria-current="page">Dashboard</li>
                </ol>
            </nav>

            <div className="db-filter-by">
                Filter by
                <div className="form-group mb-0 mx-3">
                    <select className="form-control">
                    <option>Last six month</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option>5</option>
                    </select>
                </div>
                
                <div className="form-group mb-0">
                    <select className="form-control">
                    <option>All Items</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option>5</option>
                    </select>
                </div>
            </div>
        </div>
    )
}
   
export default BreadCrumbs;