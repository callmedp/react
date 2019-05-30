import React,{Component} from 'react';
import Modal from 'react-modal';
import './addSuggestion.scss';

Modal.setAppElement(document.getElementById('react-app'));

export default class AddSuggesion extends Component{

    render(){
        const {label,modal_status,closeModal,suggestions} = this.props
        return(
            <Modal 
                isOpen={modal_status} 
                contentLabel="AddSuggested Summary"
                className="Modal"
                onRequestClose={closeModal}
                overlayClassName="Overlay">
                
                <div className="Modal--summary">
                    <p className="add text-center">Add from suggested {label}</p>
                    <div className="Modal--summary--white-box">
                        {suggestions.map((el)=>{
                                return(
                                    <div className="Modal--summary--add">
                                        <p>{el}</p>
                                        <div className="btn btn__blue">
                                        <input type="checkbox" id="add1" />
                                        <label htmlFor="add1">ADD</label>
                                        </div>
                                    </div>
                                )
                            }
                            )
                        }
                    </div>
                </div>
            </Modal>
        )
    }
}