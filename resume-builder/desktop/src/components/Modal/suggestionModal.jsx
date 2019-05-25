import React from 'react';
import Modal from 'react-modal';
import './suggestionModal.scss'

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
                    <div className="pr suggested-summary">
                        <i onClick={this.closeModal} className='icon-close icon-close--position'></i>
                        <h2>Add from suggested summary</h2>
                        <ul>
                            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(el => {
                               return( <li>
                                <span className="">
                                    <input type="checkbox" name=""/> Add
                                </span>
                               <p>Took concepts and produced design mockups and prototypes to strengthen designs, enhance user experiences and improve site interactions.</p>
                                </li>)
                            })}
                        </ul>
                        <button className="orange-button"
                                type={'submit'}>Save and Continue</button>
                    </div>
                </Modal>
            </div>
        );
    }
}