import React, {Component} from 'react'
import {connect} from 'react-redux'
import * as actions from '../../../../../store/template/actions/index'


class Template extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        let {userInfo:{selected_template}} = this.props;
        console.log(this.props)
        console.log(selected_template)
        if(selected_template){
            this.props.fetchTemplate(selected_template)
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.userInfo.selected_template != prevProps.userInfo.selected_template) {
            this.props.fetchTemplate(this.props.userInfo.selected_template)
        }
    }

    render() {
        console.log("Rendered")
        console.log(this.props)
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
        "fetchTemplate": (template) => {
            return dispatch(actions.fetchTemplate({template}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Template)