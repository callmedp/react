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
        this.handleClick = this.handleClick.bind(this);
        this.handleSuggestion = this.handleSuggestion.bind(this);
        this.state = {
            selectedArray: []
        }
    }

    handleClick(index) {
        let {selectedArray} = this.state;
        const ind = selectedArray.indexOf(index);
        if (ind > -1) {
            selectedArray = selectedArray.filter(el => el !== index)
        } else {
            selectedArray.push(index)
        }
        this.setState({
            selectedArray: selectedArray
        })

    }

    handleSuggestion() {
        const {selectedArray} = this.state;
        this.props.handleSuggestionSubmit(selectedArray);
        this.setState({
            selectedArray: []
        })

    }

    closeModal() {
        this.props.hideSuggestionModal()
    }

    render() {
        const {ui: {suggestionModal, suggestions, suggestionType}, handleSuggestionSubmit} = this.props;
        const {selectedArray} = this.state;
        console.log('---', selectedArray);

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
                        <h2>Add from suggested {suggestionType}</h2>
                        <ul>
                            {(suggestions || []).map((el, index) => {
                                return (<li>
                                <span className={selectedArray.indexOf(index) > '-1' ? 'selected' : ''}>
                                    <input onClick={() => this.handleClick(index)} type="checkbox" name=""/> Add
                                </span>
                                    <p>{el}</p>
                                </li>)
                            })}
                        </ul>
                        <button className="orange-button"
                                type={'submit'} onClick={this.handleSuggestion}>Save and Continue
                        </button>
                    </div>
                </Modal>
            </div>
        );
    }
}