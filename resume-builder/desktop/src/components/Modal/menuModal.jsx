import React from 'react';
import Modal from 'react-modal';
import {Link} from 'react-router-dom';
import "./menuModal.scss"

Modal.setAppElement(document.getElementById('react-app'));

export default class MenuModal extends React.Component {

    constructor(props){
        super(props)
        this.state ={
            preferenceList:[],
            loader:false
        }
        this.addItem = this.addItem.bind(this)
        this.removeItem = this.removeItem.bind(this)
        this.saveMenuItems = this.saveMenuItems.bind(this)
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }
    componentDidMount(){
        const {preferenceList} = this.props;
        if(preferenceList.length){
            this.setState({preferenceList})
        }
    }
    componentDidUpdate(prevProps){
        const {preferenceList} = this.props;
        if(preferenceList !== prevProps.preferenceList){
            this.setState({preferenceList})
        }
    }

    addItem(pos) {
        let {preferenceList} = this.state;
        preferenceList[pos -1].active = true;
        this.setState({preferenceList})
    }

    removeItem(pos) {
        let {preferenceList} = this.state;
        preferenceList[pos -1].active = false
        this.setState({preferenceList})
    }

    async saveMenuItems(){
        this.setState({loader:true})
        const {updateCategoryEntity,closeMenuModal} = this.props
        const {preferenceList} = this.state
        await updateCategoryEntity(preferenceList)
        this.setState({loader:false})
        closeMenuModal()
    }


    render() {
        const {menu_modal_status,closeMenuModal,formCategoryList} = this.props;
        const {preferenceList,loader} = this.state
        return (
            <div className="pr scrollynone">
                <Modal
                style={{
                            content: {
                            left: '0',
                            right: '0',
                            top: '3%',
                            bottom: '0',
                            width: '415px',
                            margin: 'auto',
                            height: '570px',
                            padding:'0',
                            overflow:'none'
                        }
                    }}
                    isOpen={menu_modal_status} 
                    contentLabel="Menu Modal"
                >
                    <div className="menu-wrap">
                        <div className="edit-section-menu">
                            <strong>Add / remove sections in your resume</strong>
                            <ul className="enable">
                                {preferenceList.filter(item =>item.active ===true && item.entity_id !==11 && item.entity_id !==6 && item.entity_id !==1).map((item, key) =>
                                    {   const {icon} = formCategoryList[item['entity_id']];
                                        return(
                                            <li key={key}>
                                                <a className={'menu-anchor'}>
                                                    <span className={`mr-20 ${icon}`}></span>
                                                    {item.entity_text}
                                                </a>
                                                {!!(item['entity_id'] !== 1 && item['entity_id'] !== 6) ?
                                                    <span className="icon-closemenu pull-right mt-20 menu-delete"  
                                                            onClick={this.removeItem.bind(this,item.entity_id)}
                                                    ></span>:''
                                                }
                                            </li>
                                        )
                                    }
                                
                                )}
                            </ul>
                            <ul className="disable">
                                {preferenceList.filter(item =>item.active ===false && item.entity_id !==11).map((item, key) =>
                                        {   const {icon} = formCategoryList[item['entity_id']];
                                            return(
                                                <li key={key}>
                                                    <a className={'menu-anchor'}>
                                                        <span className={`mr-20 ${icon}`}></span>
                                                        {item.entity_text}
                                                    </a>
                                                    <span className="icon-add pull-right mt-20 menu-add" 
                                                        onClick={this.addItem.bind(this,item.entity_id)}></span>
                                                </li>
                                            )
                                        }
                                
                                    )}
                            </ul>
                        </div>

                        <div className="flex-container menu-btm-button">
                            <button className="blue-button mr-10" type="button" disabled={loader ? true : false} onClick={closeMenuModal}>Cancel</button>
                            <button className="orange-button" type="submit"onClick={this.saveMenuItems}>
                                Done
                                {loader ?
                                    <img alt={"Menu Loading"} className="menu-loading" src={`${this.staticUrl}react/assets/images/loading-button.gif`}/>:''
                                }
                            </button>
                        </div>
                    </div>

                </Modal>
            </div>
        );
    }
}