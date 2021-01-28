import React from 'react';
import { Collapse } from 'react-bootstrap';

const ViewDetailModal = (props) => {
    const { id, toggleDetails, isOpen, datalist } = props;

    return (
        <Collapse in={isOpen == id}>
        <div className="db-view-detail arrow-box left-big" id={`openViewDetail`+id}>
        <span className="btn-close" onClick={() => toggleDetails(id)}>&#x2715;</span>
            <ul className="db-timeline-list">
                { 
                    datalist?.map((det, ind) => {
                        return (
                            <li key={ind}>
                                <i className="db-timeline-list--dot"></i>
                                <span>{det.date}</span>
                                <p className="db-timeline-list--text">{det.status}</p>
                            </li>
                        )
                    })
              
                }
            </ul>
        </div>
    </Collapse>
    )
}

export default ViewDetailModal;