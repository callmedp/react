import React from 'react';

const UploadResume = (props) => {
    const { setShowUpload } = props
    return (
        <div className="m-slide-modal">
            <div className="text-center">
                <span onClick={() => setShowUpload(false)} className="m-db-close">X</span>
                <h2>Upload Resume </h2>
                <p>To initiate your services, <strong>upload resume</strong></p>
                <div className="d-flex align-items-center justify-content-center mt-20">
                    <div className="m-upload-btn-wrapper">
                        <button className="btn btn-blue-outline">Upload a file</button>
                        <input type="file" name="myfile" />
                    </div>

                    <span className="mx-4">Or</span>

                    <div className="m-custom">
                        <input type="checkbox" id="shineResume" />
                        <label className="m-custom--label font-weight-bold mb-0" htmlFor="shineResume">Use shine resume</label>
                    </div>
                </div>

                <hr className="my-20" />

                <div className="m-db-upload-resume">
                    <strong>Select services</strong> for which you want to use this resume
                    <ul className="m-db-upload-resume--list">
                        <li className="m-custom">
                            <input type="checkbox" id="resumeBooster" />
                            <label className="font-weight-bold" htmlFor="resumeBooster">Resume Booster 5-10 years</label>
                        </li>

                        <li className="m-custom">
                            <input type="checkbox" id="resumeBuilder" />
                            <label className="font-weight-bold" htmlFor="resumeBuilder">Resume Builder 5-10 yrs</label>
                        </li>

                        <li className="m-custom">
                            <input type="checkbox" id="services" />
                            <label className="font-weight-bold" htmlFor="services">For all services</label>
                        </li>
                    </ul>
                </div>

                <button className="btn btn-primary px-5 mt-30">Save</button>
            </div>

        </div>
    )
}

export default UploadResume;