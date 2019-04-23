import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";
import {formCategoryList, entityList} from "../../../../../Utils/formCategoryList";
import {connect} from 'react-redux'
import * as actions from '../../../../../store/personalInfo/actions/index'

class Edit extends Component {
    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.addMoreClick = this.addMoreClick.bind(this);
        this.deleteFromVisibleList = this.deleteFromVisibleList.bind(this);
        this.addIntoVisibleList = this.addIntoVisibleList.bind(this);
        const values = queryString.parse(this.props.location.search);
        this.state = {
            type: (values && values.type) || '',
            show: false,
            preferenceList: this.props.entityList
        };

        if (!(values && values.type)) {
            this.props.history.push('/resume-builder/edit/?type=profile')
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    addMoreClick() {
        this.setState({
            show: true
        })
    }

    componentDidMount() {
        this.props.fetchEntityInfo()
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

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
        console.log('--props---', prevProps.entityList, this.props.entityList);
        if (this.props.entityList !== prevProps.entityList) {
            this.setState({
                preferenceList: this.props.entityList

            })

        }
    }

    render() {
        const {type, show, preferenceList} = this.state;
        return (
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                    {
                        (preferenceList || []).filter(elem => elem.active === true).map((elem, index) => {
                            const {name, link, icon, itemType} = formCategoryList[elem['entity_id']];
                            return (
                                <li key={index} className={type === itemType ? 'edit-section--active' : ''}>
                                    <Link to={link}>
                                        <span className={'mr-20 ' + icon}></span>
                                        {name}
                                    </Link>
                                    <span onClick={() => this.deleteFromVisibleList(elem)}
                                          className="icon-delete pull-right"/>
                                </li>
                            )
                        })
                    }
                    {
                        !!(!show) && !!(preferenceList.filter(elem => elem.active !== true).length) &&
                        <li className="edit-section--addmore mt-30" onClick={this.addMoreClick}>
                            + Add more sections
                        </li>
                    }
                    {!!(show) &&
                    (preferenceList || []).filter(elem => elem.active !== true).map((elem, index) => {
                        const {name, link, icon, itemType} = formCategoryList[elem['entity_id']];
                        return (
                            <li key={index} className={type === itemType ? 'edit-section--active' : ''}>
                                <Link to={link}>
                                    <span className={'mr-20 ' + icon}></span>
                                    {name}
                                </Link>
                                <span onClick={() => this.addIntoVisibleList(elem)}
                                      className="icon-add pull-right"/>
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
        entityList: state.personalInfo && state.personalInfo.entity_preference_data || []
    }
}

const mapDispatchToProps = (dispatch) => {
    return {

        "fetchEntityInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        'updateCategoryEntity': (entity) => {
            return dispatch(actions.updateEntityPreference({"entity_preference_data": entity}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Edit)

