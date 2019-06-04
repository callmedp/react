import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement(document.getElementById('react-app'));

export default class MenuModal extends React.Component {


    render() {

        return (
            <div className="pr scrollynone">
                <Modal
                style={{
                        content: {
                            left: '0',
                            right: '0',
                            top: '3%',
                            bottom: '0',
                            width: '400px',
                            margin: 'auto',
                            height: '570px',
                            padding:'0',
                        }
                    }}
                    isOpen={false} 
                    contentLabel="Menu Modal"
                >
                    <div class="edit-section-menu">
                        <strong>Add / remove sections in your resume</strong>
                        <ul className="enable">
                            <li><a href="/resume-builder/edit/?type=profile"><span className="mr-20 icon-info"></span>Personal Info</a></li>
                            <li><a href="/resume-builder/edit/?type=education"><span className="mr-20 icon-education"></span>Education</a><span className="icon-closemenu pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=experience"><span className="mr-20 icon-experience"></span>Experience</a><span className="icon-closemenu pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=project"><span className="mr-20 icon-projects"></span>Projects</a><span className="icon-closemenu pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=skill"><span className="mr-20 icon-skills"></span>Skill</a><span className="icon-closemenu pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=summary"><span className="mr-20 icon-summary"></span>Summary</a></li></ul>
                         <ul className="disable">  <li><a href="/resume-builder/edit/?type=award"><span className="mr-20 icon-awards"></span>Achievements</a><span className="icon-add pull-right mt-20"></span></li>
                            <li ><a href="/resume-builder/edit/?type=course"><span className="mr-20 icon-courses"></span>Certifications</a><span className="icon-add pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=language"><span className="mr-20 icon-languages"></span>Languages</a><span className="icon-add pull-right mt-20"></span></li>
                            <li><a href="/resume-builder/edit/?type=reference"><span className="mr-20 icon-references"></span>References</a><span className="icon-add pull-right mt-20"></span></li>
                       </ul >
                    </div>
                    <div className="flex-container menu-btm-button"><button className="blue-button mr-10" type="button">Cancel</button><button className="orange-button" type="submit">Done</button></div>
                </Modal>
            </div>
        );
    }
}