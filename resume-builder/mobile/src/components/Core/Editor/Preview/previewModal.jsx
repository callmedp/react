import React,{Component} from 'react';
import Modal from 'react-modal';
import './preview.scss'

Modal.setAppElement(document.getElementById('react-app'));

export default class PreviewModal extends Component{

    render(){
        return(
            <Modal 
                isOpen={this.props.template.modal_status} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="Modal"
                overlayClassName="Overlay">
                <div className="Modal--iframe">
                    <iframe srcDoc={this.props.template.html}></iframe>
                </div>
                <button className="Modal--close" onClick={()=>{this.props.updateModalStatus({modal_status:false})}}>+</button>
            </Modal>
        )
    }

    
}