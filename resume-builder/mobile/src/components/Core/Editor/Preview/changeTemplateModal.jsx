import React,{Component} from 'react';
import Modal from 'react-modal';
import './preview.scss'
import ResumeSlider from '../../Home/ResumeSlider/resumeSlider';

Modal.setAppElement(document.getElementById('react-app'));

export default class ChangeTemplateModal extends Component{

    render(){
        return(
            <Modal 
                isOpen={this.props.template.modal_status} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="Modal overflow-visible"
                overlayClassName="Overlay">
                <div className="">
                    <ResumeSlider showtext={false} {...this.props}/>
                </div>
                <span className="close-wrap preview-close" onClick={()=>{this.props.updateModalStatus({modal_status:false})}}>
                    <i className="sprite icon--close"></i>
                </span>
            </Modal>
        )
    }
}