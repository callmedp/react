import React from 'react';
import './haveQuery.scss';
import { contactData } from 'utils/constants';

   
const HaveQuery = (props) => {
    const { contactNo, contactEmail, contactTimings } = contactData
    return(
        <div className="m-have-query">
            <h2 className="m-have-query--curve">Have a Query</h2>

            <ul>
                <li className="m-call-us"><a href={`tel:${contactNo}`}>{ contactNo }</a></li>
                <li className="m-mail-us"><a href={`mailto: ${contactEmail}`}>{ contactEmail }</a></li>
                <li className="m-timing">Timings - <strong>{ contactTimings }</strong></li>
            </ul>
        </div>
    )
}
   
export default HaveQuery;