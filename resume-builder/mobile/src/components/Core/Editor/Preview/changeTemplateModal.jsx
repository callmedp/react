import React,{Component} from 'react';
import Modal from 'react-modal';
import './preview.scss'
import ResumeSlider from '../../Home/ResumeSlider/resumeSlider';

Modal.setAppElement(document.getElementById('react-app'));

export default class ChangeTemplateModal extends Component{

    render(){
        return(
            <Modal 
                isOpen={this.props.initialValues.modal_status} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="Modal"
                overlayClassName="Overlay">
                <div className="Modal--iframe">
                    <ResumeSlider showtext={false} {...this.props}/>
                </div>
                <button className="Modal--close" onClick={()=>{this.props.updateModalStatus({modal_status:false})}}>+</button>
            </Modal>
        )
    }

    
}