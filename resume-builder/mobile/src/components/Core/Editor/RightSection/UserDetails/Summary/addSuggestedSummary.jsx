import React,{Component} from 'react';
import Modal from 'react-modal';

Modal.setAppElement(document.getElementById('react-app'));

export default class ChangeTemplateModal extends Component{

    render(){
        return(
            <Modal 
                isOpen={true} 
                contentLabel="AddSuggested Summary"
                className="Modal"
                overlayClassName="Overlay">
                
                <div className="Modal--summary">
                    <p className="add text-center">Add from suggested summary</p>
                    <div className="Modal--summary--white-box">
                        <div className="Modal--summary--add">
                            <p>Took concepts and produced design mockups and prototypes to strengthen designs, enhance user experiences and improve site interactions.</p>
                            <div className="btn btn__blue">
                            <input type="checkbox" id="add1" />
                            <label for="add1">ADD</label>
                            </div>
                        </div>
                        
                        <div className="Modal--summary--add">
                            <p>Spearheaded production of page content such as visuals and text copy to meet project specifications.</p>
                            <div className="btn btn__blue">
                            <input type="checkbox" id="add2" />
                            <label for="add2">ADD</label>
                            </div>
                        </div>
                        
                        <div className="Modal--summary--add">
                            <p>Spearheaded production of page content such as visuals and text copy to meet project specifications.</p>
                            <div className="btn btn__blue">
                            <input type="checkbox" id="add3" />
                            <label for="add3">ADD</label>
                            </div>
                        </div>

                        <div className="text-center mb-15">
                            <a href="#" className="btn btn__round btn__primary">Save & Continue</a>
                        </div>
                    </div>
                </div>
            </Modal>
        )
    }
}