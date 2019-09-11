import React, {Component} from 'react';
import Modal from 'react-modal';
import './addSuggestion.scss';
import {renderAsyncCreatableSelect} from '../../FormHandler/formFieldRenderer';

if(typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}

export default class AddSuggesion extends Component {
    constructor(props) {
        super(props);
        this.state = {
            suggestion_selected: {},
            error: false,
            length: 0
        }
        this.addSuggesion = this.addSuggesion.bind(this);
        this.removeSuggesion = this.removeSuggesion.bind(this)
        this.handleSuggestion = this.handleSuggestion.bind(this)
    }

    addSuggesion(el, index, event) {
        event.preventDefault()
        let {suggestion_selected} = this.state
        const {maxLength} = this.props
        const {length} = this.state
        if (length + el.length > maxLength) {
            this.setState({error: true})
            return
        }
        suggestion_selected[`${index}`] = el
        this.setState({suggestion_selected, error: false, length: length + el.length})

    }

    componentDidMount() {
        const {length} = this.props
        this.setState({length})
    }

    componentDidUpdate(prevProps) {
        const {length} = this.props
        if (length !== prevProps.length) {
            this.setState({length})
        }
    }

    removeSuggesion(index, event) {
        event.preventDefault()
        let {suggestion_selected, length} = this.state
        this.setState({error: false, length: length - suggestion_selected[`${index}`]})
        delete suggestion_selected[`${index}`]
        this.setState({suggestion_selected})
    }

    handleSuggestion(suggestion_selected) {
        this.props.closeModal(suggestion_selected);
        this.setState({suggestion_selected: {}, error: false})
    }

    render() {
        const {label, modal_status, closeModal, suggestions, maxLength} = this.props
        const {suggestion_selected, error} = this.state
        return (
            <Modal
                isOpen={modal_status}
                contentLabel="AddSuggested Summary"
                className="Modal"
                onRequestClose={() => this.handleSuggestion({})}
                overlayClassName="Overlay">

                <div className={"Modal--summary " + (suggestions.length ? '' : "d-flex align-items-center")}>
                    {suggestions.length ?
                        <React.Fragment>
                            <p className="add text-center">Add from suggested {label}</p>
                            <div className="Modal--summary--white-box">
                                {suggestions.map((el, index) => {
                                        return (
                                            <div className="Modal--summary--add" key={index}>
                                                <p>{el}</p>
                                                <div className="btn btn__blue" onClick={(event) => {
                                                    suggestion_selected[index]
                                                        ? this.removeSuggesion(index, event) : this.addSuggesion(el, index, event)
                                                }}>
                                                    <input type="checkbox" readOnly
                                                           checked={suggestion_selected[index] ? true : false}
                                                           id={`add${index}`}/>
                                                    <label htmlFor={`add${index}`}>ADD</label>
                                                </div>
                                            </div>
                                        )
                                    }
                                )
                                }
                            </div>
                            {error ?
                                <p className="suggestion-error">Sorry this Suggestion cannot be added.It exceeds the
                                    maximum {maxLength} characters length of summary</p> : ''}

                            <div className="text-center Modal--summary--bottom-ctc">
                                <a className="btn btn__round btn__primary" onClick={() => {
                                    this.handleSuggestion(suggestion_selected)
                                }}>Save & Continue</a>
                            </div>
                        </React.Fragment> :
                        <div className="Modal--summary--white-box sorry-popup">
                            <p className=" text-center no-suggestion">Sorry suggestion not available for this job
                                title</p>
                            <div className="text-center mb-15">
                                <a className="btn btn__medium btn__round btn__primary" onClick={() => {
                                    this.handleSuggestion(suggestion_selected)
                                }}>Close</a>
                            </div>
                        </div>
                    }

                </div>
            </Modal>
        )
    }
}