import React, {Component} from 'react';
import {Field, FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/award/actions";
import {connect} from "react-redux";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/award/validate";
import {AwardRenderer} from "./awardRenderer";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import {scroller} from "react-scroll/modules";

class Award extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteAward = this.deleteAward.bind(this);

        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false

        }
        this.props.currentForm('award');
    }

    componentDidMount() {
        this.props.fetchUserAward()
    }


    componentWillUnmount() {
        let {formData: {award: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)));
        if (!error && !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list'])

    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }
    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            order: listLength
        })

        scroller.scrollTo(`award${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 200,
            containerId: 'award'
        })
    }

    deleteAward(index, fields, event) {
        event.stopPropagation();
        const award = fields.get(index);
        fields.remove(index);
        if (award && award.id) {
            this.props.removeAward(award.id)
        }
    }

    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit, ui: {loader}, saveTitle, editHeading,
            isEditable, entityName, handleInputValue, nextEntity, handlePreview, changeOrderingDown, changeOrderingUp
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name="list"
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteAward={this.deleteAward}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={AwardRenderer}
                            saveTitle={(event) => saveTitle(event, 7)}
                            editHeading={(value) => editHeading(value)}
                            entityName={entityName}
                            isEditable={isEditable}
                            handleInputValue={handleInputValue}
                            expanded={this.state.active}
                />
                <div className={'flex-container items-right mr-20 mb-30'}>
                    <button className={'blue-button mr-10'} type={'button'}
                            onClick={handlePreview}>Preview
                    </button>
                    <button className={'orange-button'}
                            type={'submit'}>{!nextEntity ? "Download" : 'Save and Continue'}</button>
                </div>

            </form>
        )
    }
}


export const AwardForm = reduxForm({
    form: 'award',
    validate,
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'award',-100),
})(Award);


const mapStateToProps = (state) => {
    return {
        initialValues: state.award,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userAward) => {
            const {date} = userAward;

            userAward = {
                ...userAward,
                ...{
                    date: (date && moment(date).format('YYYY-MM-DD')) || '',
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserAward({userAward, resolve, reject}));
            })
        },
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
        "removeAward": (awardId) => {
            return dispatch(actions.deleteAward(awardId))
        },

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userAward, index) => {
                const {date} = userAward;
                if (!userAward['id']) delete userAward['id'];
                userAward = {
                    ...userAward,
                    ...{
                        date: (date && moment(date).format('YYYY-MM-DD')) || '',
                        order: index
                    }
                };
                return userAward;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserAward({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);
