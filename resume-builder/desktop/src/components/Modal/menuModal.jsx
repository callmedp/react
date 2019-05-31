import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement(document.getElementById('react-app'));

export default class MenuModal extends React.Component {


    render() {

        return (
            <div className="pr">
                <Modal
                    isOpen={false} 
                    contentLabel="Menu Modal"
                >
                    <strong>Complete your information</strong>
                    <ul>
                        
                    </ul>
                </Modal>
            </div>
        );
    }
}