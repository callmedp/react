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
                        }
                    }}
                    isOpen={false} 
                    contentLabel="Menu Modal"
                >
                    <div class="edit-section-menu">
                        <strong>Add / remove sections in your resume</strong>
                        <ul>
                            <li class=""><a href="/resume-builder/edit/?type=profile"><span class="mr-20 icon-info"></span>Personal Info</a></li>
                            <li class=""><a href="/resume-builder/edit/?type=education"><span class="mr-20 icon-education"></span>Education</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=experience"><span class="mr-20 icon-experience"></span>Experience</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=project"><span class="mr-20 icon-projects"></span>Projects</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=skill"><span class="mr-20 icon-skills"></span>Skill</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=summary"><span class="mr-20 icon-summary"></span>Summary</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=award"><span class="mr-20 icon-awards"></span>Achievements</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=course"><span class="mr-20 icon-courses"></span>Certifications</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=language"><span class="mr-20 icon-languages"></span>Languages</a><span class="icon-closemenu pull-right mt-20"></span></li>
                            <li class=""><a href="/resume-builder/edit/?type=reference"><span class="mr-20 icon-references"></span>References</a><span class="icon-closemenu pull-right mt-20"></span></li>
                        </ul>
                    </div>
                    <div class="flex-container menu-btm-button"><button class="blue-button mr-10" type="button">Cancel</button><button class="orange-button" type="submit">Done</button></div>
                </Modal>
            </div>
        );
    }
}