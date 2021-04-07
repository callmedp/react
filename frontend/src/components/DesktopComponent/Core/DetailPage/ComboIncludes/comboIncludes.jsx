import React from 'react';
import './comboIncludes.scss';
import {Link} from 'react-router-dom';

const ComboIncludes = (props) => {

    return (
        <div className="combo-includes mt-20">
            <h2 className="heading2">Combo includes</h2>
            <ul className="combo-includes__list">
                <li><Link to={"#"}>Featured Profile : 30 Days</Link></li>
                <li><Link to={"#"}>AWS Architect Certification Training</Link></li>
            </ul>
        </div>
    )
}

export default ComboIncludes;