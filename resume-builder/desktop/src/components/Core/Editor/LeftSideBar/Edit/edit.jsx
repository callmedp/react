import React, {Component, Fragment} from 'react';
import {Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";
import {formCategoryList, entityList} from "../../../../../Utils/formCategoryList";
import {connect} from 'react-redux'
import * as actions from '../../../../../store/personalInfo/actions/index'
import {showMoreSection, showAlertModal, hideAlertModal} from '../../../../../store/ui/actions/index'
import Swal from 'sweetalert2'
import AlertModal from '../../../../Modal/alertModal.jsx'

class Edit extends Component {
    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.addMoreClick = this.addMoreClick.bind(this);
        this.deleteFromVisibleList = this.deleteFromVisibleList.bind(this);
        this.addIntoVisibleList = this.addIntoVisibleList.bind(this);
        this.showErrorMessage = this.showErrorMessage.bind(this);
        this.handleDeleteClick = this.handleDeleteClick.bind(this);
        this.state = {
            preferenceList: this.props.entityList,
            nextLink: '',
            elementToDelete: null
        };
    }


    handleSpanClick(e) {
        e.stopPropagation();
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

    addMoreClick() {
        this.props.showMoreSection()
    }

    addIntoVisibleList(addedElem) {
        const updatedList = (this.state.preferenceList || []).map(elem => {
            if (elem['entity_id'] === addedElem['entity_id']) {
                return {
                    ...elem,
                    ...{active: true}
                }
            }
            return elem;
        });
        this.props.updateCategoryEntity(updatedList);
        this.setState({
            preferenceList: updatedList
        })
    }

    deleteFromVisibleList(deletedElem) {
        const updatedList = (this.state.preferenceList || []).map(elem => {
            if (elem['entity_id'] === deletedElem['entity_id']) {
                return {
                    ...elem,
                    ...{active: false}
                }
            }
            return elem;
        })
        this.props.updateCategoryEntity(updatedList);
        this.setState({
            preferenceList: updatedList
        })
    }

    showErrorMessage(link) {
        this.setState({
            nextLink: link
        })
        this.props.showAlertModal('error');
        const {ui: {formName}} = this.props;
        // Swal.fire({
        //     title: 'Are you sure?',
        //     text: `Some information may be lost as required fields are not filled.`,
        //     type: 'warning',
        //     showCancelButton: true,
        //     confirmButtonColor: '#3085d6',
        //     cancelButtonColor: '#d33',
        //     confirmButtonText: 'Yes, change it!'
        // }).then((result) => {
        //     if (result.value) {
        //         this.props.history.push(link)
        //     }
        // })
    }

    handleDeleteClick(elem) {
        this.setState({
            elemToDelete: elem
        })
        this.props.showAlertModal('delete');

        // Swal.fire({
        //     text: "Do you really want to remove this section?",
        //     type: 'warning',
        //     showCancelButton: true,
        //     confirmButtonColor: '#3085d6',
        //     cancelButtonColor: '#d33',
        //     confirmButtonText: 'Confirm'
        // }).then((result) => {
        //     if (result.value) {
        //         this.deleteFromVisibleList(elem);
        //     }
        // })

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

    render() {
        const {type, preferenceList, nextLink, elemToDelete} = this.state;
        let {formData, ui: {formName, showMoreSection}} = this.props;
        let error = false;
        const obj = formData && formData[formName] || {};
        let syncErrors = obj['syncErrors'] || {};
        if ('fields' in obj) {
            if ('list' in syncErrors) (syncErrors && syncErrors['list'] || []).map(el => (el ? Object.keys(el) : []).map(key => (!!el[key] ? error = true : false)))
            else Object.keys(syncErrors || {}).map(key => (!!syncErrors[key] ? error = true : false));
        }
        return (
            <div className="edit-section">
                <AlertModal {...this.props}
                            nextLink={nextLink}
                            elemToDelete={elemToDelete}
                            deleteFromVisibleList={this.deleteFromVisibleList}
                />
                <strong>Complete your information</strong>
                <ul>
                    {
                        (preferenceList || []).filter(elem => elem.active === true).map((elem, index) => {
                            const {link, icon, itemType} = formCategoryList[elem['entity_id']];
                            return (
                                <li key={index}
                                    className={showMoreSection ? 'disabled' : '' + (type === itemType ? ' edit-section--active' : '')}>
                                    {
                                        !!(error || showMoreSection) ?
                                            <div onClick={() => this.showErrorMessage(link)} className={"non-link"}>
                                                <span className={'mr-20 ' + icon}></span>
                                                {elem['entity_text']}
                                            </div>
                                            :
                                            <Link to={link}>
                                                <span className={'mr-20 ' + icon}></span>
                                                {elem['entity_text']}
                                            </Link>
                                    }
                                    {
                                        !!(elem['entity_id'] !== 1 && elem['entity_id'] !== 6) ?
                                            <span onClick={() => this.handleDeleteClick(elem)}
                                                  className="icon-delete pull-right mt-20"/> : ''
                                    }
                                </li>
                            )
                        })
                    }
                    {
                        !!(!showMoreSection) && !!(preferenceList.filter(elem => elem.active !== true).length) &&
                        <li className="edit-section--addmore mt-30" onClick={this.addMoreClick}>
                            + Add more sections
                        </li>
                    }
                    {!!(showMoreSection) &&
                    (preferenceList || []).filter(elem => elem.active !== true).map((elem, index) => {
                        const {link, icon, itemType} = formCategoryList[elem['entity_id']];
                        return (
                            <li key={index} className={type === itemType ? 'edit-section--active' : ''}>
                                <div className={"non-link"}>
                                    <span className={'mr-20 ' + icon}></span>
                                    {elem['entity_text']}
                                </div>
                                <span onClick={() => this.addIntoVisibleList(elem)}
                                      className="icon-add pull-right mt-20"/>
                            </li>
                        )
                    })
                    }
                </ul>
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
            return dispatch(actions.updateEntityPreference({"entity_preference_data": entity}))
        },
        'showMoreSection': () => {
            return dispatch(showMoreSection())
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

