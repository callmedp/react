import React from 'react';
import { Link } from 'react-router-dom';
import './personalDetail.scss';

const EditSkills = (props) => {
    return(
        <div className="personal-detail">
            <div className="personal-detail__heading">
                <button className="m-db-btn-close"></button>
                <h2>Skills</h2>
                <Link to={"#"} className="personal-detail__heading--save">Save</Link>
            </div>

            <div className="m-container">
                <div className="m-enquire-now personal-detail__form">
                    <ul>
                        <li className="m-form-group">
                            <input type="text" id="name" className="m-form-control" name="name"  placeholder=" " aria-required="true" aria-invalid="true" value="Data Science" />
                            <label className="input-label" for="">Skills</label>
                        </li>
                    </ul>

                    <div className="m-skills-tag m-add-skill">
                        <span>Data Science</span>
                        <span>ERP Management</span>
                        <span>Six Sigma</span>
                    </div>
                </div>
            </div>

            

            
        </div>
    )

}

export default EditSkills;