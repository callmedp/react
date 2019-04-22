import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";
import {formCategoryList, entityList} from "../../../../../Utils/formCategoryList";

export default class Edit extends Component {
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
            hiddenList: [],
            visibleList: []
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

    addIntoVisibleList(addedElem) {
        let visList = this.state.visibleList;
        visList.push(addedElem);
        let hidList = this.state.hiddenList.filter(elem => elem.itemType !== addedElem.itemType)
        console.log('----', visList, hidList)
        this.setState({
            visibleList: visList,
            hiddenList: hidList
        })
    }

    deleteFromVisibleList(deletedElem) {
        let hidList = this.state.hiddenList;
        hidList.push(deletedElem);
        let visList = this.state.visibleList.filter(elem => elem.itemType !== deletedElem.itemType)
        this.setState({
            visibleList: visList,
            hiddenList: hidList
        })
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
    }

    render() {
        const {type, show, visibleList, hiddenList} = this.state;
        console.log('---entity===', entityList);

        return (
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                    {
                        (entityList || []).filter(elem => elem.active === true).map((elem, index) => {
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
                        !!(!show) &&
                        <li className="edit-section--addmore mt-30" onClick={this.addMoreClick}>
                            + Add more sections
                        </li>
                    }
                    {!!(show) &&
                    (entityList || []).filter(elem => elem.active !== true).map((elem, index) => {
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