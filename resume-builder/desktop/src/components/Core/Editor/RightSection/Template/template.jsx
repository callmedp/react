import React, {Component} from 'react'
import {connect} from 'react-redux'
import * as actions from '../../../../../store/template/actions/index'
import propTypes from 'prop-types';

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
        const {template: {html}} = this.props;
        return html ? (
            <div>
                <div className="right-sidebar-scroll-main"
                     dangerouslySetInnerHTML={{
                         __html: html
                     }}>
                </div>
            </div>
        ): null
    }

}

Template.propTypes = {
    fetchTemplate: propTypes.func,
    userInfo: propTypes.shape({
        active_subscription: propTypes.bool,
        candidate_id: propTypes.string,
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        free_resume_downloads: propTypes.number,
        gender: propTypes.object,
        id: propTypes.number,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
        selected_template: propTypes.string,
    }),
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