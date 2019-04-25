import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../.../../../../../../store/award/actions";
import {connect} from "react-redux";
import validate from "../../../../../FormHandler/validtaions/award/validate"
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import PreviewModal from "../../../Preview/previewModal";
import renderAwards from "./renderAwards"
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'


class Award extends Component {

    constructor(props){
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteAward = this.deleteAward.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserAward()
        ////console.log(this.props.sidenav)
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            //console.log("Came Here")
        }
        else{
            await this.props.bulkUpdateUserAward(values.list);
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
    }

    handleAddition(fields, error) {
        ////console.log(error)
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            order: fields.length
        })

        scroller.scrollTo(`award${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 100
        })
    }

    deleteAward(index, fields, event) {
        event.stopPropagation();
        const award = fields.get(index);
        ////console.log(award)
        fields.remove(index);
        if (award && award.id) {
            this.props.removeAward(award.id)
        }
    }

    async changeOrderingUp(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
        await this.props.bulkUpdateUserAward(fields.getAll());
    }

    async changeOrderingDown(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
        await this.props.bulkUpdateUserAward(fields.getAll());
    }

    render () {
        const {handleSubmit, award,  error, submitting, submitSucceeded, invalid} = this.props;
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        
        return(
            <div className="buildResume">
                <PreviewModal {...this.props}/>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.handleAddition}
                                deleteAward={this.deleteAward}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderAwards}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting || submitSucceeded} type={(length === pos +1) ?'button' :'submit'}
                                    onClick={(length === pos +1) ? ()=>{this.props.history.push(`/resume-builder/buy`)} : ()=>{}}>
                                    {(length === pos +1) ?"Buy" :"Save &amp; Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>

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
        award: state.award
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
            ////console.log(userAward)
            //return "yes"
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserAward({userAward, resolve, reject}));
            })
        },
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
        "removeAward": (awardId) => {
            ////console.log("Award iD   "+awardId)
            return dispatch(actions.deleteAward(awardId))
        },
        "bulkUpdateUserAward": (listItems) => {
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
            ////console.log(listItems)
            return dispatch(actions.bulkUpdateUserAward({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);