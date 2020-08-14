import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";
import { formCategoryList } from "../../../../../Utils/formCategoryList";
import { connect } from 'react-redux'
import * as actions from '../../../../../store/personalInfo/actions/index'
import { showAlertModal, hideAlertModal } from '../../../../../store/ui/actions/index'
import AlertModal from '../../../../Modal/alertModal.jsx'
import MenuModal from '../../../../Modal/menuModal';
import { eventClicked } from '../../../../../store/googleAnalytics/actions/index'
import { withRouter } from 'react-router-dom';
import propTypes from 'prop-types';

const isSame = (initialField, formField) => {
    let isSame = true;
    if (initialField instanceof Array && formField instanceof Array) {
        (initialField || []).map((el, index) => (initialField[index] === formField[index] ? true : isSame = false))
        return isSame;
    }
    if (initialField === formField) return true;
    return false;

}

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
            menu_modal_status: false,
        };
    }

    componentDidMount() {
        this.props.eventClicked({
            'action': 'Add/Edit',
            'label': 'Click'
        })
    }


    static getDerivedStateFromProps(nextProps, prevState) {
        const values = queryString.parse(nextProps.location.search);
        const entityPreferenceList = nextProps.entityList;
        const {formName} = nextProps;

        let currentEntityIndex = Object.values(formCategoryList).findIndex(item => item['itemType'] === formName);
        if (entityPreferenceList && entityPreferenceList.length) {
            if (!(entityPreferenceList[currentEntityIndex] && entityPreferenceList[currentEntityIndex].active)) {
                for (let ind = currentEntityIndex - 1; ind >= 0; ind--) {
                    if (entityPreferenceList[ind].active) {
                        nextProps.history.push(formCategoryList[ind + 1].link);
                        return null;
                    }
                }
            }
        }
        if (!(values && values.type)) {
            if (formName) {
                nextProps.history.push(`/resume-builder/edit/?type=${formName}`);
            } else nextProps.history.push('/resume-builder/edit/?type=profile');
        }
        return ({
            type: (values && values.type) || ''
        })
    }

    deleteFromVisibleList(deletedElem) {
        const updatedList = (this.state.preferenceList || []).map(elem => {
            if (elem['entity_id'] === deletedElem['entity_id']) {
                return {
                    ...elem,
                    ...{ active: false }
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

    openMenuModal() {
        this.setState({ menu_modal_status: true });
        this.props.eventClicked({
            'action': 'Add/Remove',
            'label': 'Click'
        })
    }

    closeMenuModal() {
        this.setState({ menu_modal_status: false })
    }

    render() {
        const { type, preferenceList, nextLink, elemToDelete, menu_modal_status } = this.state;
        let { formData, formName, updateCategoryEntity, showAlertModal, eventClicked, generateResumeModal,alertModal, hideAlertModal } = this.props;
        let error = [], filled = [], isError = false, isFilled = false;
        const obj = (formData && formData[formName]) || {};
        let syncErrors = obj['syncErrors'] || {};
        let values = obj['values'] || {};
        let initial = obj['initial'] || {};
        const newUser = localStorage.getItem('newUser');
        if ('fields' in obj) {
            if ('list' in syncErrors) ((syncErrors && syncErrors['list']) || []).map((el, ind) => {
                error[ind] = false;
                return (el ? Object.values(el)
                    : []).map(value => (!!value ? error[ind] = true : false))
            });
            else {
                error[0] = false;
                Object.values(syncErrors || {}).map(value => (!!value ? error[0] = true : false));
            }
            if ('list' in initial) {
                initial = initial && initial['list'][0]
            }
            if ('list' in values) ((values && values['list'] || [])).map((el, index) => {
                filled[index] = false;
                return (el ? Object.keys(el) : []).map(
                    key => (isSame(initial[key], el[key]) ? false : filled[index] = true)
                )
            }
            )
            else {
                filled[0] = false;
                Object.keys(values || {}).map(key => (isSame(initial[key], values[key]) ? false : filled[0] = true))
            }

            // Currently only feasible for single item in any list
            for (let ind = 0; ind < error.length; ind++) {
                if (error[ind] && filled[ind]) {
                    isError = true;
                    isFilled = true;
                    break;
                }
            }
        }

        return (
            <div className="edit-section">
                <MenuModal
                    eventClicked={eventClicked}
                    menu_modal_status={menu_modal_status}
                    closeMenuModal={this.closeMenuModal}
                    preferenceList={preferenceList}
                    formCategoryList={formCategoryList}
                    updateCategoryEntity={updateCategoryEntity}
                />
                <AlertModal 
                    alertModal = {alertModal}
                    generateResumeModal = {generateResumeModal}
                    nextLink={nextLink}
                    elemToDelete={elemToDelete}
                    newUser={newUser}
                    hideAlertModal = {hideAlertModal}
                />
                <strong>Complete your information</strong>
                <ul>
                    {
                        (preferenceList || []).filter(elem => elem.active === true).map((elem, index) => {
                            const { link, icon, itemType, name } = formCategoryList[elem['entity_id']];
                            return (
                                <li key={elem['entity_id']}
                                    className={(type === itemType ? ' edit-section--active' : '')}>
                                    {
                                        !!((isError && isFilled) || newUser) ?
                                            (
                                                <div onClick={() => this.showErrorMessage(link)}
                                                    className={"non-link"}>
                                                    <span className={'mr-20 ' + icon}></span>
                                                    {elem['entity_text']}
                                                </div>

                                            )

                                            :

                                            (
                                                <Link to={link}
                                                    onClick={() => {
                                                        eventClicked({
                                                            'action': 'SelectSection',
                                                            'label': name
                                                        })
                                                    }}>
                                                    <span className={'mr-20 ' + icon}></span>
                                                    {elem['entity_text']}
                                                </Link>
                                            )
                                    }
                                    {
                                        !!(elem['entity_id'] !== 1 && elem['entity_id'] !== 6) ?
                                            <span onClick={() => this.deleteFromVisibleList(elem)}
                                                className="icon-closemenu pull-right mt-20" /> : ''
                                    }
                                </li>
                            )
                        })
                    }
                </ul>

                <div className="edit-section--addmore" onClick={() => {
                    newUser ? showAlertModal('error') : this.openMenuModal()
                }}>
                    + Add more sections
                </div>
            </div>
        )
    }

}

Edit.propTypes = {
    entityList: propTypes.array,
    eventClicked: propTypes.func,
    updateCategoryEntity: propTypes.func,
    showAlertModal: propTypes.func,
    hideAlertModal: propTypes.func,
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
    formData: propTypes.object,
    formName: propTypes.string,
    generateResumeModal: propTypes.bool,
    alertModal: propTypes.bool,
}

const mapStateToProps = (state) => {
    return {
        entityList: (state.personalInfo && state.personalInfo.entity_preference_data) || [],
        formName: (state.ui && state.ui.formName) || '',
        formData: state && state.form,
        alertModal: (state.ui && state.ui.alertModal) || false,
        generateResumeModal: (state.ui && state.ui.generateResumeModal) || false,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        'updateCategoryEntity': (entity, showLoader = true) => {
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateEntityPreference({
                    "entity_preference_data": entity, showLoader,
                    resolve, reject
                }))
            })
        },
        'showAlertModal': (alertType) => {
            return dispatch(showAlertModal(alertType))
        },
        'hideAlertModal': () => {
            return dispatch(hideAlertModal())
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },

    }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Edit))

