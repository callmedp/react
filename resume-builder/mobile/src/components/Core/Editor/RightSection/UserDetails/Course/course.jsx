import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import moment from "moment";
import PreviewModal from "../../../Preview/previewModal";
import renderCourse from "./renderCourse";
import validate from "../../../../../FormHandler/validtaions/course/validate"
import {siteDomain} from "../../../../../../Utils/domains";


class Course extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteCourse = this.deleteCourse.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : '',
            'submit' : false
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.editHeadingClick = this.editHeadingClick.bind(this);
    }
    
    componentDidMount() {
        console.log("Inside Course")
        this.props.fetchUserCourse()
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[7].entity_text})
        }
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        this.setState({submit:true})
        await this.props.bulkUpdateUserCourse(values.list);
         if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            if(this.props.personalInfo.subscription_status){
                window.location.href = `${siteDomain}/dashboard/myorder`
            }
            else{
                this.props.history.push(`/resume-builder/buy`) 
            }
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    deleteCourse(index, fields, event) {
        event.stopPropagation();
        const course = fields.get(index);
        fields.remove(index);
        if (course && course.id) {
            this.props.removeCourse(course.id)
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
        await this.props.bulkUpdateUserCourse(fields.getAll());
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,7,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,7,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[7].entity_text})
        }
    }

    componentWillUnmount() {

        if(!this.state.submit){
            const form_data = this.props.info.form.course;
            let error = false
            let error_values =form_data["syncErrors"]
            if(error_values){
                for(let i of  error_values['list']){
                    for(let j of Object.keys(i)){
                        if(i[j]){
                            error =true
                            break;
                        }
                    }
                }
            }
            if(!error){
                this.props.bulkUpdateUserCourse(form_data['values']['list'])
            }
        }
    }

    editHeadingClick(){
        this.setState({editHeading:true})
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
        await this.props.bulkUpdateUserCourse(fields.getAll());
    }

    render () {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const {handleSubmit, course,submitting,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        const {subscription_status} = this.props.personalInfo;
        return(

            <div className="buildResume">
                <PreviewModal {...this.props}/>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" 
                                handleSubmit={handleSubmit}
                                handleAddition={this.props.handleAddition}
                                deleteCourse={this.deleteCourse}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderCourse}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                loader={this.props.loader.dataloader}
                                heading ={heading}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true});this.props.fetchTemplate()}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const CourseForm = reduxForm({
    form: 'course',
    enableReinitialize: true,
    validate
})(Course);


const mapStateToProps = (state) => {
    return {
        initialValues: state.course,
        course: state.course
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userCourse) => {
            const {year_of_certification} = userCourse;
            userCourse = {
                ...userCourse,
                ...{
                    year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                }
            };
            ////console.log(userCourse)
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserCourse({userCourse, resolve, reject}));
            })
        },
        "fetchUserCourse": () => {
            return dispatch(actions.fetchUserCourse())
        },
        "removeCourse": (courseId) => {
            return dispatch(actions.deleteCourse(courseId))
        },

        "bulkUpdateUserCourse": (listItems) => {
            listItems = (listItems || []).map(userCourse => {
                const {year_of_certification} = userCourse;
                if (!userCourse['id']) delete userCourse['id'];
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                    }
                };
                return userCourse;
            })
            return dispatch(actions.bulkUpdateUserCourse({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CourseForm);
