import React from 'react';
import './haveQuery.scss';

   
const HaveQuery = (props) => {
    return(
        <div className="container have-query-wrap">
            <div className="have-query">
                <h2 className="have-query--curve">Have a Query</h2>

                <ul>
                    <li className="call-us"><a href="#">08047105151</a></li>
                    <li className="mail-us"><a href="#">resume@shine.com</a></li>
                    <li className="timing d-none d-xl-block">Timings - <strong>9:00am to 6:30pm (Mon - Sat)</strong></li>
                </ul>
            </div>
        </div>
    )
}
   
export default HaveQuery;