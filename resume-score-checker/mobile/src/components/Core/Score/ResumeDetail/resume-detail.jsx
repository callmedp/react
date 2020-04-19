import React from 'react';
import { useSelector } from 'react-redux';
import './resume-detail.scss';

export default function ResumeDetail() {
    const localValue = JSON.parse(localStorage.getItem('resume_score'))
    const storeValue = useSelector(state => state.uploadFile['section_score'])

    const section_score = localStorage.getItem('resume_score') === null ? storeValue : localValue['section_score']
    const toggle = (event) => (event.checked = !(event.checked))

    const Description = (description) => { return {__html: description} };

    return(
            <div className="pb-30">
                <div className="resume-detail mb-15">
                    <h2><span>Resume detailed review</span></h2>
                </div>
            {
                section_score ?
                (<div className="container-box">
                    <div className="tabs">
                        {
                            section_score.map((value, index) => (
                                <div className="tab" key={index} onClick={(event) => toggle(event.target.firstChild)}>
                                    <input type="radio" id={index} name="rd" defaultChecked = {false}></input>
                                    <label className="tab-label">
                                    {(value['section_status'] === 2) ? <i className = "sprite green-tick mr-10 mt-5"></i> : (value['section_status'] === 0) ? <i className="sprite question-mark mr-10 mt-5"></i> : <i className="sprite caution-mark mr-10 mt-5"></i>}
                                        <div className="d-flex flex-direction-column">
                                            <p className="d-block pb-0 font-weight-semiBold">{value['section_name']}</p>
                                            <p className="d-block pb-0 fs-12"><strong className="fs-14">{value['section_score']}</strong>/{value['section_total_score']}</p>
                                        </div>                               
                                    </label>
                                    <div className="tab-content">
                                        <div dangerouslySetInnerHTML={Description(value['section_description'])} />
                                    </div>
                                </div>
                            ))
                        }
                    </div>

                    <ul className="indicators d-flex mt-20">
                        <li className="d-flex">
                            <i className="sprite green-tick mr-5"></i>
                            <span>Available in resume</span>
                        </li>
                        <li>
                            <i className="sprite question-mark mr-5"></i>
                            <span>Missing in resume</span>
                        </li>
                        <li>
                            <i className="sprite caution-mark mr-5"></i>
                            <span>Need major attention</span>
                        </li>
                    </ul>
                </div>):null}
            </div>
    );
}