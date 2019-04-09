import React, {Component} from 'react'
import {connect} from 'react-redux'
import * as actions from '../../../../../store/template/actions/index'


class Template extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.props.fetchTemplate()
    }

    render() {
        const {template: {html}} = this.props;
        return (
            <div className="right-sidebar-scroll-main"
                 dangerouslySetInnerHTML={{
                     __html: html
                 }}/>
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
        "fetchTemplate": () => {
            return dispatch(actions.fetchTemplate())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Template)