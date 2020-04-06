import React from 'react';
import { useSelector } from 'react-redux';
import './resume-detail.scss';

export default function ResumeDetail() {
    const section_score = useSelector(state => state.uploadFile.section_score)

    const toggle = (event) => (event.checked = !(event.checked))

    return(
            <div className="pb-30">
                <div className="resume-detail mb-15">
                    <h2><span>Resume detailed review</span></h2>
                </div>
            {
                section_score == undefined ?  null:
                (<div className="container-box">
                    <div className="tabs">
                        {
                            section_score.map((value, index) => (
                                <div className="tab" key={index} onClick={(event) => toggle(event.target.firstChild)}>
                                    <input type="radio" id={index} name="rd" checked = {false}></input>
                                    <label className="tab-label">
                                    {(value.section_status == 1) ? <i className="sprite green-tick mr-10 mt-5"></i> : (value.section_status == 2) ? <i className="sprite question-mark mr-10 mt-5"></i> : <i className="sprite caution-mark mr-10 mt-5"></i>}
                                        <div className="d-flex flex-direction-column">
                                            <p className="d-block pb-0 font-weight-semiBold">{value.section_name}</p>
                                            <p className="d-block pb-0 fs-12"><strong className="fs-14">{value.section_score}</strong>/{value.total_section_score}</p>
                                        </div>                               
                                    </label>
                                    <div className="tab-content">
                                        <br></br>
                                        <p>{value.section_description}</p>

                                        <ul className="blue-bullet mt-15 mb-20">
                                            <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                            <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                            <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                        </ul>
                                    </div>
                                </div>
                            ))
                        }
                        

                        {/* <div className="tab">
                            <input type="radio" id="rd2" name="rd"></input>
                            <label className="tab-label" htmlFor="rd2">
                                <i className="sprite question-mark mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Summary &amp; Objective</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="tab">
                            <input type="radio" id="rd3" name="rd"></input>
                            <label className="tab-label" htmlFor="rd3">
                                <i className="sprite caution-mark mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Accomplishments</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="tab">
                            <input type="radio" id="rd4" name="rd"></input>
                            <label className="tab-label" htmlFor="rd4">
                                <i className="sprite green-tick mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Education Details</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="tab">
                            <input type="radio" id="rd5" name="rd"></input>
                            <label className="tab-label" htmlFor="rd5">
                                <i className="sprite green-tick mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Work Experience</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="tab">
                            <input type="radio" id="rd6" name="rd"></input>
                            <label className="tab-label" htmlFor="rd6">
                                <i className="sprite green-tick mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Skills</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div>

                        <div className="tab">
                            <input type="radio" id="rd7" name="rd"></input>
                            <label className="tab-label" htmlFor="rd7">
                                <i className="sprite green-tick mr-10 mt-5"></i>
                                <div className="d-flex flex-direction-column">
                                    <p className="d-block pb-0 font-weight-semiBold">Contact Details</p>
                                    <p className="d-block pb-0 fs-12"><strong className="fs-14">40</strong>/100</p>
                                </div>                               
                            </label>
                            <div className="tab-content">
                                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>

                                <ul className="blue-bullet mt-15 mb-20">
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting ind an unknown printer took a galley of type and scrambled it to make a type.</li>
                                    <li>Lorem Ipsum is simply dummy text of the printing and typesetting industry</li>
                                    <li>Ipsum has been the industry's standard dummy text ever since the 1500s.</li>
                                </ul>
                            </div>
                        </div> */}

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
                </div>)}
            </div>
    );
}