import React, {useState} from 'react';
import './breadcrumb.scss';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions';
import { useDispatch } from 'react-redux';
   
const BreadCrumbs = (props) => {
    const {filterState, setfilterState} = props;

    const FilterChecks = async(e) => {
        const name = e.target.name;
        const value = e.target.value;
        setfilterState({ ...filterState, [name]: value });
      };

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
                    <select className="form-control" onChange={(e) => FilterChecks(e)}
                    name="last_month_from"
                    value={filterState.last_month_from}>
                        <option value="18">Last eighteen months</option>
                        <option value="6">Last six months</option>
                        <option value="3">Last three months</option>
                    </select>
                </div>
                
                <div className="form-group mb-0">
                    <select className="form-control" onChange={(e) => FilterChecks(e)}
                    name="select_type"
                    value={filterState.select_type}>
                        <option value="all">All Items</option>
                        <option value="2">In Process</option>
                        <option value="3">Closed</option>
                    </select>
                </div>
            </div>
        </div>
    )
}
   
export default BreadCrumbs;