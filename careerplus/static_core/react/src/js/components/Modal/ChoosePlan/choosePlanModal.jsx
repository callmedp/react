import Modal from 'react-modal';
import React from 'react';

export default class ChoosePlanModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showModal: false
        };
    }

    render() {
        const {closeModal, showModal} = this.props;
        return (
            <div>
                <Modal
                    isOpen={showModal}
                    contentLabel="Minimal Modal Example"
                >
                    <div className={'Choose-plan'}>
                        <div className={'Template-images'}>

                        </div>
                        <div className={'Go-to-pricing'}>
                            <span>To download your file<br/> choose one of our plans</span>
                            <span>You are just one step away from getting your job winning resume.<br/>
                    Tip: The template you selected is available in Start</span>
                            <button onClick={closeModal}>GO TO PRICING</button>
                        </div>
                    </div>
                </Modal>
            </div>
    );
    }
    }