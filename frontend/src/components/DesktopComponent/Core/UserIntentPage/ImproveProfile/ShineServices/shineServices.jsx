import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import './shineServices.scss';


const ShineServices = (props) => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="completed" to={"#"}>2</Link>
                        </div>
                        <h2 className="heading3 mt-20">Get an edge over others with shine services</h2>
                        <div className="shine-services w-70">
                            <figure className="icon-upload-resume"></figure>
                            <p>Updated resume increases the chances of getting more opportunities. </p>
                            <Link to={"#"} onClick={handleShow} className="ml-auto">Upload latest resume</Link>
                        </div>
                        <div className="shine-services w-70">
                            <figure className="icon-update-profile"></figure>
                            <p>Update your profile to get customised career recommendation </p>
                            <Link to={"#"} className="ml-auto">Update your profile</Link>
                        </div>

                        <h2 className="heading3 mt-50">Recommended services</h2>
                        <div className="w-70">
                            <div className="row recommend-services">
                                <div className="col">
                                    <div className="services-foryou">
                                        <h3 className="heading3">Resume Writing</h3>
                                        <p>Resume written by experts to increase your profile visibility</p>
                                        <span className="d-flex">
                                            <Link to={"#"}>Know more</Link>
                                            <figure className="icon-service1"></figure>
                                        </span>
                                    </div>
                                </div>
                                <div className="col">
                                    <div className="services-foryou">
                                        <h3 className="heading3">Featured Profile</h3>
                                        <p>Appear on top when Recruiters search for best candidates</p>
                                        <span className="d-flex">
                                            <Link to={"#"}>Know more</Link>
                                            <figure className="icon-service2"></figure>
                                        </span>
                                    </div>
                                </div>
                                <div className="col">
                                    <div className="services-foryou">
                                        <h3 className="heading3">Jobs on the Move</h3>
                                        <p>Get personalized job recommend -ations from all the job portals on your Whatsapp</p>
                                        <span className="d-flex">
                                            <Link to={"#"}>Know more</Link>
                                            <figure className="icon-service3"></figure>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Modal show={show} 
                onHide={handleClose}
                {...props}
                // size="md"
                dialogClassName="resume-upload-box"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                
                <Modal.Header closeButton>
                </Modal.Header>
                <Modal.Body>
                    <h2 className="mb-20">Upload Resume</h2>
                    <form className="mt-10">
                        <p>increases the chances of getting more opportunities, with latest resume</p>
                        <div class="upload-btn-wrapper mt-5">
                            <button class="btn-upload">Choose file<input type="file" name="myfile" /></button>
                            
                        </div>
                        <span className="d-block mt-10">File size should not exceed 3MB. in .doc, PDF, Jpeg format only</span>
                        <button type="submit" className="btn btn-primary submit-btn mx-auto mt-30" role="button">Save</button>
                    </form>
                </Modal.Body>
            </Modal>
        </section>
    )
}

export default ShineServices;