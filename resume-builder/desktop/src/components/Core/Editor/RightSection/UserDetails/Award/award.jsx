import React, {Component} from 'react';
import './award.scss'
import {Field, FieldArray, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/award/actions";
import {connect} from "react-redux";
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import validate from "../../../../../FormHandler/validations/award/validate";
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';
import Loader from "../../../../../Loader/loader.jsx";

const AwardRenderer = ({
                           fields,
                           loader,
                           meta: {touched, error, submitFailed},
                           handleSubmit,
                           deleteAward,
                           handleAddition,
                           handleAccordionState,
                           handleAccordionClick,
                           changeOrderingUp,
                           changeOrderingDown,
                           openedAccordion,
                           isEditable,
                           editHeading,
                           saveTitle,
                       }) => {
    let elem = null;
    return (
        <div>
            {!!(loader) &&
            <Loader/>
            }
            <section className="head-section">
                <span className="icon-box"><i className="icon-awards1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}
                >Awards</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-awards__cursor" : ""}/>

                <button onClick={handleSubmit((values) => {
                    handleAddition(fields, error)
                })}
                        type={'button'}
                        className="add-button add-button__right">Add new
                </button>

            </section>
            <section className="right-sidebar-scroll">
                <ul>
                    <Accordion
                        onChange={(value) => handleAccordionClick(value, fields, error)}
                        allowZeroExpanded={true}
                        preExpanded={[openedAccordion]}
                    >
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).title || 'Award'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteAward(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                {index !== 0 &&
                                                                <span
                                                                    onClick={(event) => changeOrderingUp(index, fields, event)}
                                                                    className="icon-ascend mr-5"/>
                                                                }
                                                                {
                                                                    index !== fields.length - 1 &&
                                                                    < span
                                                                        onClick={(event) => changeOrderingDown(index, fields, event)}
                                                                        className="icon-descend"/>
                                                                }
                                                            </div>
                                                        </div>
                                                    </AccordionItemButton>
                                                </AccordionItemHeading>
                                                <AccordionItemPanel>
                                                    <div className="flex-container">
                                                        <fieldset className="error">
                                                            <label>Title</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-awards-gr"/>
                                                                </div>
                                                                <Field component={renderField} type={"text"}
                                                                       name={`${member}.title`}
                                                                       className="input-control"/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker} type={"date"}
                                                                       className={'input-control'}
                                                                       name={`${member}.date`}/>
                                                            </div>
                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Summary</label>
                                                            <Field component={renderTextArea} type={"textarea"}
                                                                   name={`${member}.summary`}
                                                                   className="input-control"/>
                                                        </fieldset>
                                                    </div>
                                                </AccordionItemPanel>
                                            </AccordionItem>
                                        </section>
                                    </li>
                                )
                            })
                        }
                    </Accordion>
                </ul>
            </section>


        </div>
    )
}

class Award extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteAward = this.deleteAward.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.saveTitle = this.saveTitle.bind(this);
        this.editHeading = this.editHeading.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
            isEditable: false


        }
    }

    componentDidMount() {
        this.props.fetchUserAward()
    }


    editHeading(elem) {
        this.setState({
            'isEditable': true
        });
        setTimeout(() => {
            elem.focus()
        }, 0)


    }

    saveTitle(event) {
        event.stopPropagation();
        if (event.keyCode === 13) {
            this.setState({
                'isEditable': false
            })
        }
    }

    async handleSubmit(values) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
            this.props.history.push('/resume-builder/edit/?type=course')
        }
    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem]);
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])
    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        if (listLength) this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            order: fields.length
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

    handleAccordionState(val, fields) {
        const {currentAccordion} = this.state;

        if (currentAccordion !== '') {
            this.props.onSubmit(fields.get(currentAccordion))
        }

        this.setState((state) => ({
            previousAccordion: state.currentAccordion,
            openedAccordion: val,
            currentAccordion: val
        }))
    }

    handleAccordionClick(value, fields) {
        const val = value.length > 0 ? value[0] : '';
        this.handleAccordionState(val, fields)
    }


    render() {
        const {handleSubmit, ui: {loader}} = this.props;


        return (
            <form onSubmit={handleSubmit(this.handleSubmit)}>
                <FieldArray name="list"
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAccordionState={this.handleAccordionState}
                            handleAddition={this.handleAddition}
                            deleteAward={this.deleteAward}
                            changeOrderingUp={this.changeOrderingUp}
                            changeOrderingDown={this.changeOrderingDown}
                            openedAccordion={this.state.openedAccordion}
                            component={AwardRenderer}
                            saveTitle={(event) => this.saveTitle(event)}
                            editHeading={(value) => this.editHeading(value)}
                            isEditable={this.state.isEditable}
                />
                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button" type={'submit'}>Save & Continue</button>
                </div>

            </form>
        )
    }
}


export const AwardForm = reduxForm({
    form: 'award',
    validate,
    enableReinitialize: true
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

        "handleSwap": (listItems) => {
            listItems = (listItems || []).map(userAward => {
                const {date} = userAward;
                if (!userAward['id']) delete userAward['id'];
                userAward = {
                    ...userAward,
                    ...{
                        date: (date && moment(date).format('YYYY-MM-DD')) || '',
                    }
                };
                return userAward;
            })
            return dispatch(actions.handleAwardSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);
