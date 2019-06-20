import React, {Component} from 'react'
import {connect} from 'react-redux'
import * as actions from '../../../../../store/template/actions/index'


class Template extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        let {userInfo: {selected_template}} = this.props;
        if (selected_template) {
            this.props.fetchTemplate(selected_template)
        }

    }

    componentDidUpdate(prevProps) {
        if (this.props.userInfo.selected_template != prevProps.userInfo.selected_template) {
            this.props.fetchTemplate(this.props.userInfo.selected_template)
        }
    }

    render() {
        const {template: {templateToPreview}} = this.props;
        return (
            <div>
                <div className="right-sidebar-scroll-main">
                    <img src={`data:image/png;base64,${templateToPreview}`}/>
                </div>
            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        template: state.template
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": (template) => {
            return dispatch(actions.fetchTemplate({template}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Template)