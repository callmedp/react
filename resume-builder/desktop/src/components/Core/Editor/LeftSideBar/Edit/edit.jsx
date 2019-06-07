import React, {Component, Fragment} from 'react';
import {Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";
import {formCategoryList, entityList} from "../../../../../Utils/formCategoryList";
import {connect} from 'react-redux'
import * as actions from '../../../../../store/personalInfo/actions/index'
import {showAlertModal, hideAlertModal} from '../../../../../store/ui/actions/index'
import AlertModal from '../../../../Modal/alertModal.jsx'
import MenuModal from '../../../../Modal/menuModal';

class Edit extends Component {
    constructor(props) {
        super(props);
        this.showErrorMessage = this.showErrorMessage.bind(this);
        this.openMenuModal = this.openMenuModal.bind(this);
        this.closeMenuModal = this.closeMenuModal.bind(this);
        this.state = {
            preferenceList: this.props.entityList,
            nextLink: '',
            elementToDelete: null,
            menu_modal_status: false
        };
        
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const values = queryString.parse(nextProps.location.search);
        const {ui: {formName}} = nextProps;
        if (!(values && values.type)) {
            if (formName) {
                nextProps.history.push(`/resume-builder/edit/?type=${formName}`);
            } else nextProps.history.push('/resume-builder/edit/?type=profile');
        }
        return ({
            type: values && values.type || ''
        })
    }


    showErrorMessage(link) {
        this.setState({
            nextLink: link
        })
        this.props.showAlertModal('error');
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
        if (this.props.entityList !== prevProps.entityList) {
            this.setState({
                preferenceList: this.props.entityList

            })
        }
    }

    openMenuModal(){
        this.setState({menu_modal_status:true})
    }
    closeMenuModal(){
        this.setState({menu_modal_status:false})
    }

    render() {
        const {type, preferenceList, nextLink, elemToDelete,menu_modal_status} = this.state;
        let {formData, ui: {formName},updateCategoryEntity} = this.props;
        let error = false;
        const obj = formData && formData[formName] || {};
        let syncErrors = obj['syncErrors'] || {};
        const newUser = localStorage.getItem('newUser')
        if ('fields' in obj) {
            if ('list' in syncErrors) (syncErrors && syncErrors['list'] || []).map(el => (el ? Object.keys(el) : []).map(key => (!!el[key] ? error = true : false)))
            else Object.keys(syncErrors || {}).map(key => (!!syncErrors[key] ? error = true : false));
        }
        return (
            <div className="edit-section">
                <MenuModal 
                    menu_modal_status={menu_modal_status}
                    closeMenuModal={this.closeMenuModal}
                    preferenceList={preferenceList}
                    formCategoryList={formCategoryList}
                    updateCategoryEntity={updateCategoryEntity}
                />
                <AlertModal {...this.props}
                            nextLink={nextLink}
                            elemToDelete={elemToDelete}
                            newUser={newUser}
                />
                <strong>Complete your information</strong>
                <ul>
                    {
                        (preferenceList || []).filter(elem => elem.active === true).map((elem, index) => {
                            const {link, icon, itemType} = formCategoryList[elem['entity_id']];
                            return (
                                <li key={index}
                                    className={(type === itemType ? ' edit-section--active' : '')}>
                                    {
                                        !!(error || newUser) ?
                                            <div onClick={() => this.showErrorMessage(link)} className={"non-link"}>
                                                <span className={'mr-20 ' + icon}></span>
                                                {elem['entity_text']}
                                            </div>
                                            :
                                            <Link to={link} >
                                                <span className={'mr-20 ' + icon}></span>
                                                {elem['entity_text']}
                                            </Link>
                                    }
                                </li>
                            )
                        })
                    }
                </ul>

                <div className="edit-section--addmore" onClick={this.openMenuModal}>
                    + Add/Remove sections
                </div>
        </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        entityList: state.personalInfo && state.personalInfo.entity_preference_data || [],
        ui: state.ui,
        formData: state && state.form
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        'updateCategoryEntity': (entity) => {
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateEntityPreference({"entity_preference_data": entity,resolve,reject}))
            })
        },
        'showAlertModal': (alertType) => {
            return dispatch(showAlertModal(alertType))
        },
        'hideAlertModal': () => {
            return dispatch(hideAlertModal())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Edit)

