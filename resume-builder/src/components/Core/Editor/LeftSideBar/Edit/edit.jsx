import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import './edit.scss'
import queryString from "query-string";

let visibleList = [
    {
        name: 'Personal Info',
        link: '/resume-builder/edit/?type=profile',
        icon: 'icon-info',
        itemType: 'profile'
    },
    {
        name: 'Summary',
        link: '/resume-builder/edit/?type=summary',
        icon: 'icon-summary',
        itemType: 'summary'


    },
    {
        name: 'Experience',
        link: '/resume-builder/edit/?type=experience',
        icon: 'icon-experience',
        itemType: 'experience'


    },
    {
        name: 'Education',
        link: '/resume-builder/edit/?type=education',
        icon: 'icon-education',
        itemType: 'education'

    },
    {
        name: 'Skills',
        link: '/resume-builder/edit/?type=skill',
        icon: 'icon-skills',
        itemType: 'skill'


    },

];

let hiddenList = [
    {
        name: 'Languages',
        link: '/resume-builder/edit/?type=language',
        icon: 'icon-languages',
        itemType: 'language'
    },
    {
        name: 'Awards',
        link: '/resume-builder/edit/?type=award',
        icon: 'icon-awards',
        itemType: 'award'


    },
    {
        name: 'Courses',
        link: '/resume-builder/edit/?type=course',
        icon: 'icon-courses',
        itemType: 'course'


    },
    {
        name: 'Projects',
        link: '/resume-builder/edit/?type=project',
        icon: 'icon-projects',
        itemType: 'project'

    },
    {
        name: 'References',
        link: '/resume-builder/edit/?type=reference',
        icon: 'icon-references',
        itemType: 'reference'


    },
];

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
            hiddenList: hiddenList,
            visibleList: visibleList
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
        hidList.push(deletedElem)
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
        return (
            <div className="edit-section">
                <strong>Complete your information</strong>
                <ul>
                    {
                        (visibleList || []).map((elem, index) => {
                            const {name, link, icon, itemType} = elem;
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
                    (hiddenList || []).map((elem, index) => {
                        const {name, link, icon, itemType} = elem;
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