import React from 'react';
import './haveQuery.scss';

   
const HaveQuery = (props) => {
    return(
        <div className="m-have-query">
            <h2 className="m-have-query--curve">Have a Query</h2>

            <ul>
                <li className="m-call-us"><a href="#">08047105151</a></li>
                <li className="m-mail-us"><a href="#">resume@shine.com</a></li>
                <li className="m-timing">Timings - <strong>9:00am to 6:30pm (Mon - Sat)</strong></li>
            </ul>
        </div>
    )
}
   
export default HaveQuery;