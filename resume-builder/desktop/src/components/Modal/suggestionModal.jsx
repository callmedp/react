import React from 'react';
import Modal from 'react-modal';
import './templateModal.scss'

Modal.setAppElement(document.getElementById('react-app'));


// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)

export default class SuggestionModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.closeModal = this.closeModal.bind(this);
    }

    closeModal() {
        this.props.hideSuggestionModal()
    }

    render() {
        const {ui: {suggestionModal}} = this.props;
        return (
            <div className="pr">
                <Modal
                    style={{
                        content: {
                            left: '10%',
                            right: '10%',
                            top: '15%',
                            bottom: '0',
                        }
                    }}
                    isOpen={suggestionModal}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div className="pr">
                        <i onClick={this.closeModal} className='icon-close icon-close--position'></i>
                        <ul>
                            {[1, 2, 3, 4, 5, 6, 7].map(el => {
                               return( <li>el</li>)
                            })}
                        </ul>
                    </div>
                </Modal>
            </div>
        );
    }
}