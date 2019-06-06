import React,{Component} from 'react';
import Modal from 'react-modal';
import './alert.scss'


Modal.setAppElement(document.getElementById('react-app'));

export default class AreYouSure extends Component{

    constructor(props){
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }
    render(){
        const {modal_status,templateImage} = this.props;
        return(
            <Modal 
                isOpen={true} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="alertModal"
                overlayClassName="Overlay">
                <div className="alertModal__wrap">
                    <i className="sprite icon--alert m-auto"></i>
                    <div className="alertModal__wrap--title text-center mb-15">Are you sure?</div>
                    <div className="alertModal__wrap--content text-center mb-15">
                        <p>Some information may be lost as required fields are not filled.</p>
                    </div>
                    <div className="alertModal__wrap__btn-wrap">
                        <span className="btn btn-sm btn__primary btn__round w-150">Yes, change it!</span>
                        <span className="btn btn-sm btn--outline btn__round w-150">Cancel</span>
                    </div>
                </div>
            </Modal>
        )
    }
}