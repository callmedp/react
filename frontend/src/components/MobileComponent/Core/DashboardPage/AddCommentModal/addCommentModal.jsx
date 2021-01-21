import React, { useEffect, useState } from 'react';

const AddCommentModal = (props) => {
    const { setShowCommentModal }  = props

    return (
        <div className="m-slide-modal">

            <div className="">
                <span className="m-db-close" onClick={() => {setShowCommentModal(false)}}>X</span>
                <br />
                <ul className="m-timeline-list">
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                        <p className="m-timeline-list--text">Need help to understand this service.</p>
                    </li>
                    
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                        <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                    </li>
                    
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                        <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                    </li>
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                        <p className="m-timeline-list--text">Need help to understand this service.</p>
                    </li>
                    
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                        <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                    </li>
                    
                    <li>
                        <i className="m-timeline-list--dot"></i>
                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                        <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                    </li>
                </ul>
                <hr />
                <div className="m-enquire-now mt-15 text-center">
                    <div className="m-form-group">
                        <textarea id="addComments" placeholder=" " rows="4"></textarea>
                        <label htmlFor="addComments">Enter comment here</label>
                    </div>
                    <button className="btn btn-blue">Submit</button>
                </div>
            </div>

        </div>
    )
}

export default AddCommentModal