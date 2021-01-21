import React from 'react';
import { Collapse } from 'react-bootstrap';

const ViewDetailModal = (props) => {

    const { id, toggleDetails, isOpen } = props;

    return (
        <Collapse in={isOpen == id}>
        <div className="db-view-detail arrow-box left-big" id={`openViewDetail`+id}>
        <span className="btn-close" onClick={() => toggleDetails(id)}>&#x2715;</span>
            <ul className="db-timeline-list">
                <li>
                    <i className="db-timeline-list--dot"></i>
                    <span>Dec. 11, 2020</span>
                    <p className="db-timeline-list--text">Need help to understand this service.</p>
                </li>  
            </ul>
        </div>
    </Collapse>
    )
}

export default ViewDetailModal;