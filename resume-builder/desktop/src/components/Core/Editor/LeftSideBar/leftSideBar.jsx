import React, { Component, PureComponent } from 'react';
import './leftSideBar.scss'
import Edit from './Edit/edit.jsx'
import Preview from './Preview/preview.jsx'
import { Link } from 'react-router-dom'
import propTypes from 'prop-types';

export default class LeftSideBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            edit: true
        };
        this.activateEditTab = this.activateEditTab.bind(this);
        this.activatePreviewTab = this.activatePreviewTab.bind(this);
        this.previewClicked = this.previewClicked.bind(this);
        const path = this.props.match.path;
        if (path === '/resume-builder/edit/') {
            this.state.edit = true;
        }
        else this.state.edit = false;
    }

    activateEditTab() {
        this.setState({
            edit: true
        })

    }

    activatePreviewTab() {
        this.setState({
            edit: false
        })
    }

    previewClicked() {
        const { previewButtonClicked, eventClicked } = this.props;
        previewButtonClicked(true);
        eventClicked({
            'action': 'Preview',
            'label': 'SideNav'
        })
    }


    render() {
        const isEdit = this.state.edit;
        const newUser = localStorage.getItem('newUser')
        const {
            showAlertModal,
            onChange,
            eventClicked,
            customizeTemplate,
            generateResumeAlert,
            fetchDefaultCustomization,
            userInfo: { selected_template },
            reorderSection,
            ui,
            template: { entity_position, entity_id_count_mapping,text_font_size, color, heading_font_size},
        } = this.props;
        return (

            <section className="left-sidebar">

                <ul className="tab-heading">
                    <li className={
                        ' tab-heading--top-left-radius ' + (isEdit ? "active" : 'no-shadow')}>
                        <span className="icon-edit"></span>
                        <Link to="/resume-builder/edit">Add/ Edit</Link>
                    </li>
                    <li className={' tab-heading--top-right-radius ' +
                        (!isEdit ? "active" : 'no-shadow')}>
                        <span className="icon-preview"></span>
                        {newUser ? <a onClick={showAlertModal}>Preview</a> :
                            <a onClick={isEdit ? this.previewClicked : () => {
                            }}>Preview</a>
                            // <Link to="/resume-builder/preview">Preview</Link>
                        }
                    </li>
                </ul>
                {
                    isEdit ?
                        <Edit /> :
                        <Preview
                            onChange={onChange}
                            eventClicked={eventClicked}
                            customizeTemplate={customizeTemplate}
                            generateResumeAlert={generateResumeAlert}
                            ui = {ui}
                            fetchDefaultCustomization={fetchDefaultCustomization}
                            userInfo={{ selected_template }}
                            reorderSection={reorderSection}
                            template={{ entity_position, entity_id_count_mapping, color, heading_font_size, text_font_size }}
                        />
                }
            </section>
        )
    }
}

LeftSideBar.propTypes = {
    match: propTypes.shape({
        isExact: propTypes.bool,
        params: propTypes.object,
        path: propTypes.string,
        url: propTypes.string
    }),
    template: propTypes.shape({
        candidate: propTypes.number,
        candidate_id: propTypes.string,
        color: propTypes.number,
        entity_id_count_mapping: propTypes.object,
        entity_position: propTypes.string,
        heading_font_size: propTypes.number,
        html: propTypes.string,
        id: propTypes.number,
        modalTemplateImage: propTypes.string,
        template: propTypes.number,
        templateId: propTypes.number,
        templateImage: propTypes.string,
        templateToPreview: propTypes.string,
        template_no: propTypes.number,
        text_font_size: propTypes.number,
        thumbnailImages: propTypes.array
    })
}