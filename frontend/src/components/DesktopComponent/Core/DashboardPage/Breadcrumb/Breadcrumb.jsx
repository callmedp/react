import React from 'react';
import { siteDomain } from 'utils/domains';
import './breadcrumb.scss';
import { MyGA } from 'utils/ga.tracking.js';
   
const BreadCrumbs = (props) => {
    const {filterState, setfilterState, filterStateShow} = props;

    const FilterChecks = async(e) => {
        const name = e.target.name;
        const value = e.target.value;
        let index = e.nativeEvent.target.selectedIndex;
        let label = e.nativeEvent.target[index].text;
        setfilterState({ ...filterState, [name]: value });
        MyGA.SendEvent('DashboardInbox','ln_dashboard_left_menu', 'ln_my_inbox', label,'', false, true);
      };

    return(
        <div className="d-flex align-items-center justify-content-between">
            <nav aria-label="breadcrumb">
                <ol className="db-breadcrumb">
                    <li className="db-breadcrumb-item"><a href={siteDomain} role="button">Home</a></li>
                    <li className="db-breadcrumb-item active" aria-current="page">Dashboard</li>
                </ol>
            </nav>

            {filterStateShow && <div className="db-filter-by">
                Filter by
                <div className="form-group mb-0 mx-3">
                    <select className="form-control" onChange={(e) => FilterChecks(e)}
                    name="last_month_from"
                    value={filterState.last_month_from}>
                        <option value="all">All</option>
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
                        <option value="in_process">In Process</option>
                        <option value="closed">Closed</option>
                    </select>
                </div>
            </div>
            }
        </div>
    )
}
   
export default BreadCrumbs;