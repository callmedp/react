import React,{Component} from 'react';
import Modal from 'react-modal';
import './NeedHelpModal.scss'


Modal.setAppElement(document.getElementById('react-app'));

export default class NeedHelpModal extends Component{

    constructor(props){
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    }
    render(){
        const {modal_status} = this.props;
        return(
            <Modal 
                isOpen={false} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="alertModal"
                overlayClassName="Overlay">
                <div className="modal-reachus">
                    <h2>Reach out to us</h2>
                    <p>Let us know your feedback and suggestions, so we can help you build a powerful resume.</p>
                    <div className="form__group mt-20">
                        <textarea rows="6" maxlength="100" class="form__input"></textarea>
                    </div>
                    <div class="text-center">
                        <button className="btn btn__round btn__primary mt-20">
                            Submit
                        </button>
                    </div>
                    <span className="close-wrap" onClick={()=>{this.props.closeModalStatus()}}>
                        <i className="sprite icon--close"></i>
                    </span>
                </div>
                

            </Modal>
        )
    }
}