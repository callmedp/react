import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import {connect} from 'react-redux';
import RightSection from './RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";
import {siteDomain} from "../../../Utils/domains";
import LoaderPage from "../../Loader/loaderPage.jsx";
import * as actions from "../../../store/ui/actions"
import * as profileActions from "../../../store/personalInfo/actions"
import SelectTemplateModal from '../../Modal/selectTemplateModal';
import moment from 'moment'

class EditPreview extends Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.props.fetchEntityInfo();
    }


    render() {
        const {ui: {loader}, userInfo: {first_name}} = this.props;
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                {
                    !!(loader) &&
                    <LoaderPage/>
                }

                <Header userName={first_name}/>
                <div className="page-container">
                    <SelectTemplateModal {...this.props}/>
                    <TopBar {...this.props}/>
                    <section className={'flex-container mt-30'}>
                        <LeftSideBar {...this.props}/>
                        <RightSection {...this.props}/>
                    </section>
                </div>
                <Footer/>

            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        ui: state.ui,
        userInfo: state.personalInfo,
        template: state.template
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchEntityInfo": () => {
            return dispatch(profileActions.fetchPersonalInfo())
        },
        "showSelectTemplateModal": () => {
            return dispatch(actions.showSelectTemplateModal())
        },
        "hideSelectTemplateModal": () => {
            return dispatch(actions.hideSelectTemplateModal())
        },
        "updateSelectedTemplate": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails;
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'gender': (gender && gender['value']) || '',
                    'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).map(el => el.value).join(',') : extracurricular
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        }
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

