import React ,{Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './preview.scss';
import {connect} from "react-redux";
import {fetchTemplate,updateModalStatus,customizeTemplate,fetchDefaultCustomization,reorderSection,reGeneratePDF,} from "../../../../store/template/actions/index"
import {updatePersonalInfo,fetchPersonalInfo} from "../../../../store/personalInfo/actions/index"
import {updateAlertModalStatus,showGenerateResumeModal,hideGenerateResumeModal} from "../../../../store/ui/actions/index"
import Loader from '../../../Common/Loader/loader.jsx';
import ChangeTemplateModal from './changeTemplateModal.jsx';
import moment from 'moment'
import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import InputRange from 'react-input-range';
import Swal from 'sweetalert2'
import {siteDomain} from "../../../../Utils/domains";
import AlertModal from '../../../Common/AlertModal/alertModal.jsx';
import {eventClicked} from '../../../../store/googleAnalytics/actions/index'

class Preview extends Component {

    constructor(props){
        super(props)
        this.state={
            'customize' : false,
            currentTab: 1,
            selectedColor: 1,
            headingFontSize: 1,
            textFontSize: 1,
            activeSection: 'left',
            sectionEntityName: '',
            selectedEntity: '',
            startingReorderUpDowmIndex : 0,
            zoomIn: false
        }
        this.handleCustomization = this.handleCustomization.bind(this);
        this.selectSection = this.selectSection.bind(this);
        this.moveUpSection = this.moveUpSection.bind(this);
        this.moveDownSection = this.moveDownSection.bind(this);
        this.handleActiveSection = this.handleActiveSection.bind(this);
        this.handleZoomTemplate = this.handleZoomTemplate.bind(this);
        this.showReorderErrorToast = this.showReorderErrorToast.bind(this);
        this.getResume = this.getResume.bind(this);
    }

    componentWillUpdate(prevProps){
        const {template} = this.props
        if(template !== prevProps.template){

            this.setState({
                selectedColor:template.color,
                headingFontSize:template.heading_font_size -1,
                textFontSize:template.text_font_size -1 
            })
        }
    }

    componentDidUpdate(prevProps){
        const {template: {entity_position,reorderFailToast},personalInfo:{selected_template}} = this.props;
        const {selectedEntity} = this.state
        if(entity_position !== prevProps.template.entity_position){
            (entity_position && eval(entity_position) || []).map((el)=>{
                if(selectedEntity && selectedEntity['entity_id'] === el.entity_id){
                    this.setState({selectedEntity:el})
                } 
            })
        }
        if(selected_template !==prevProps.personalInfo.selected_template){
            this.props.fetchTemplate();
            this.props.fetchDefaultCustomization(selected_template);
        }
        if(reorderFailToast !== prevProps.template.reorderFailToast){
            this.showReorderErrorToast()
        }
    }

    showReorderErrorToast(){
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
          });
          
          Toast.fire({
            type: 'error',
            title: 'Sorry, this section cannot be moved.'
          })
    }


    async componentDidMount(){
        await this.props.fetchPersonalInfo();
        this.props.fetchTemplate();
        const {personalInfo:{selected_template}} = this.props
        this.props.fetchDefaultCustomization(selected_template || 1);
    }

    selectSection(section) {

        this.setState({
            sectionEntityName: section['entity_text'],
            selectedEntity: section,
            startingReorderUpDowmIndex: -1
        })

    }

    handleActiveSection(section) {
        this.setState({
            activeSection: section,
            startingReorderUpDowmIndex: 0,
            sectionEntityName:''
        })
    }

    handleZoomTemplate(){
        const {zoomIn} = this.state;
        zoomIn ? this.setState({zoomIn:false}): this.setState({zoomIn:true})
    }

    moveUpSection(selectedEntity, selectedTemplate) {

        this.props.reorderSection({
            templateId: selectedTemplate,
            info: {entity_id: selectedEntity['entity_id'], step: -1,pos:selectedEntity['pos']}
        })
    }

    moveDownSection(selectedEntity, selectedTemplate) {
        this.props.reorderSection({
            templateId: selectedTemplate,
            info: {entity_id: selectedEntity['entity_id'], step: 1,pos:selectedEntity['pos']}
        })
    }

    getResume(){
        const {personalInfo:{order_data},history,reGeneratePDF,showGenerateResumeModal,hideGenerateResumeModal} = this.props;
        if(order_data && order_data.id){
            showGenerateResumeModal()
            reGeneratePDF(order_data.id)
            setTimeout(function() {
                window.location.href = `${siteDomain}/dashboard`
                hideGenerateResumeModal()
            }, 10000);
        }
        else{
            history.push(`/resume-builder/buy`)
        }
    }

    async handleCustomization(data) {
        await this.props.customizeTemplate(data)
        this.props.fetchTemplate();
        this.setState({customize:false,currentTab:1})
    }

    render(){
        const {customize,currentTab,selectedColor,headingFontSize,textFontSize,sectionEntityName,startingReorderUpDowmIndex,zoomIn} = this.state
        const {template:{html,zoomInHtml,entity_position,entity_id_count_mapping},ui:{mainloader,alertModalStatus,generateResumeModal},personalInfo:{selected_template,order_data},history,eventClicked} = this.props
        return(
            <div className="preview">
               <Header page={'preview'} {...this.props} order_data={order_data} eventClicked={eventClicked} />
               <AlertModal modal_status={alertModalStatus|| generateResumeModal}  history={history} generateResumeModal={generateResumeModal}/>
               <ChangeTemplateModal {...this.props}/>
               
               {mainloader ? <Loader/> :""}


                 <div className="iframe__wrap">
                    <span className="sprite icon--zoom" onClick={this.handleZoomTemplate}></span>
                    {zoomIn ? 
                        <iframe srcDoc={zoomInHtml} className={"iframe-new"}></iframe>:
                        <iframe srcDoc={html} className={"iframe-new"}></iframe>
                    }
                </div>

               <div className="preview__bottom-btns pos-fixed">
                    <span className="btn btn__round btn--outline" onClick={()=>{this.setState({customize:true})}}>Customize template</span>
                    <span className="btn btn__round btn__primary" onClick={this.getResume }>Get your resume</span>
               </div>

               {customize ?
                    <div className="filter">
                            <div className="filter__overlay"></div>
                            <div className="filter__wrap">
                                
                                <div className="filter__accordion">
                                    <h2 className="filter__wrap--heading">Customize template</h2>
                                    <Accordion preExpanded={["1"]}>
                                        <AccordionItem uuid="1">
                                            <div className={"filter__accordion__card " +(currentTab === 1 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:1})}}>
                                                        <div className="filter__accordion__card__heading--left">
                                                            <i className="sprite icon--theme mr-10"></i>
                                                            <span>Change theme</span>
                                                        </div>

                                                        <div className="filter__accordion__card__heading--right">
                                                            <i className={"sprite "  +(currentTab === 1 ? "icon--minus":"icon--plus")}></i>
                                                        </div>
                                                    </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">  
                                                    <ul className="resume-color-theme">
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green"
                                                                onClick={()=>{this.setState({selectedColor:1})}}
                                                                checked={selectedColor === 1} readOnly />
                                                            <label htmlFor="green" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue"
                                                                onClick={()=>{this.setState({selectedColor:2})}} 
                                                                checked={selectedColor === 2} readOnly/>
                                                            <label htmlFor="blue" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"
                                                                onClick={()=>{this.setState({selectedColor:3})}}
                                                                checked={selectedColor === 3} readOnly/>
                                                            <label htmlFor="red" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black" 
                                                                onClick={()=>{this.setState({selectedColor:4})}}
                                                                checked={selectedColor === 4} readOnly/>
                                                            <label htmlFor="black" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"
                                                                onClick={()=>{this.setState({selectedColor:5})}} 
                                                                checked={selectedColor === 5} readOnly/>
                                                            <label htmlFor="brown" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet" 
                                                                onClick={()=>{this.setState({selectedColor:6})}} 
                                                                checked={selectedColor === 6} readOnly/>
                                                            <label htmlFor="violet" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                                            </label>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </AccordionItemPanel>
                                            </div>
                                        </AccordionItem>
                                        <AccordionItem >
                                            <div className={"filter__accordion__card " +(currentTab === 2 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:2})}}>
                                                    <div className="filter__accordion__card__heading--left">
                                                        <i className="sprite icon--font mr-10"></i>
                                                        <span>Font size</span>
                                                    </div>

                                                    <div className="filter__accordion__card__heading--right">
                                                        <i className={"sprite "  +(currentTab === 2 ? "icon--minus":"icon--plus")}></i>
                                                    </div>
                                                </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">
                                                <div className="font-filter">
                                                    {/* <h3>Section Heading</h3>
                                                    <div className="font-filter__slide-bar">
                                                        <span className="font-filter__dot"></span>
                                                        <span className="font-filter--small mt-10 fs-12">S</span>
                                                        <span className="font-filter--medium mt-10 fs-12">M</span>
                                                        <span className="font-filter--large mt-10 fs-12">L</span>
                                                    </div> */}
                                                    <h3>Section Heading</h3>
                                                    <InputRange
                                                        name = "heading_font_size"
                                                        maxValue={2}
                                                        minValue={0}
                                                        value={headingFontSize}
                                                        onChange={value => this.setState({ headingFontSize: value })} />
                                                    <div className="heading-size">
                                                        <div className="heading-size-item">S</div>
                                                        <div className="heading-size-item">M</div>
                                                        <div>L</div>
                                                    </div>
                                                    <h3>Section Text</h3>
                                                    <InputRange
                                                        name="text_font_size"
                                                        maxValue={2}
                                                        minValue={0}
                                                        value={textFontSize}
                                                        onChange={value => this.setState({ textFontSize: value })} />
                                                    <div className="heading-size">
                                                        <div className="heading-size-item">S</div>
                                                        <div className="heading-size-item">M</div>
                                                        <div>L</div>
                                                    </div>
                                                </div>
                                            </div>
                                            </AccordionItemPanel>
                                        </div>
                                        </AccordionItem>
                                        <AccordionItem >
                                            <div className={"filter__accordion__card " +(currentTab === 3 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:3})}}>
                                                    <div className="filter__accordion__card__heading--left">
                                                        <i className="sprite icon--reorder mr-10"></i>
                                                        <span>Reorder section</span>
                                                    </div>

                                                    <div            className="filter__accordion__card__heading--right">
                                                        <i className={"sprite "  +(currentTab === 3 ? "icon--minus":"icon--plus")}></i>
                                                    </div>
                                                </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">

                                                    {/* <ul className="tabs">
                                                        <li className={activeSection ==='left' ? "active":""} 
                                                            onClick={() => this.handleActiveSection('left')}>Left</li>
                                                        <li className={activeSection ==='right' ? "active":""}
                                                            onClick={() => this.handleActiveSection('right')}>Right</li>
                                                    </ul> */}
                                                    <div className="reorder">
                                                        <ul className="reorder__items">
                                                            {entity_position.filter(item => 
                                                                    (item.entity_id!==1 && item.entity_id!==6)
                                                                    && (item['active']) && entity_id_count_mapping[item['entity_id']]).map((el,index,arr)=>{
                                                                return(
                                                                        <li key={index} className={"reorder__item " + ((el['entity_text'] === sectionEntityName || startingReorderUpDowmIndex===index)? " reorder--select":"")}
                                                                            onClick={() => this.selectSection(el)} >
                                                                            <span className="reorder__title">{el.entity_text}</span>
                                                                            <div className="reorder__nav">
                                                                                {index !==0 ?
                                                                                    <span className="reorder__nav--item">
                                                                                        <i className="sprite icon--upArrow" onClick={()=>{this.moveUpSection(el,selected_template);}}></i>
                                                                                    </span>:''
                                                                                }
                                                                                {index+1 !== arr.length ? 
                                                                                    <span className="reorder__nav--item">
                                                                                        <i className="sprite icon--downArrow" onClick={()=>{this.moveDownSection(el,selected_template);}}></i>
                                                                                    </span>:''
                                                                                }
                                                                            </div>
                                                                        </li>
                                                                )
                                                                
                                                            })}
                                                        </ul> 
                                                    </div>



                                                </div>
                                            </AccordionItemPanel>
                                            </div>
                                        </AccordionItem>
                                    </Accordion>
                                </div>

                                <div className="filter__apply-btn">
                                    <span className="btn" onClick={()=>{this.setState({customize:false,currentTab:1})}}>Cancel</span>
                                    <span className="btn btn__round btn--outline" 
                                    onClick={() => this.handleCustomization({
                                                                    color: selectedColor,
                                                                    template: selected_template,
                                                                    heading_font_size: headingFontSize + 1,
                                                                    text_font_size: textFontSize + 1
                                                                })} >Apply</span>
                                </div>
                            </div>
                        </div>
                    :''
                }        
            </div>

            
        )
    }

}

const mapStateToProps = (state) => {
    return {
        template: state.template,
        ui: state.ui,
        personalInfo: state.personalInfo,
        allinfo:state
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(fetchTemplate())
        },
        'reGeneratePDF': (data) => {
            return dispatch(reGeneratePDF(data))
        },
        "updateModalStatus": (data) => {
            return dispatch(updateModalStatus(data))
        },
        "fetchPersonalInfo": (data) => {
            return dispatch(fetchPersonalInfo(data))
        },
        "customizeTemplate": (template_data) => {
            return new Promise((resolve, reject) => {
                return dispatch(customizeTemplate({template_data,resolve,reject}))
            })
        },
        "fetchDefaultCustomization": (templateId) => {
            return dispatch(fetchDefaultCustomization(templateId))
        },
        "reorderSection": (data) => {
            return dispatch(reorderSection(data))
        },
        "updateAlertModalStatus": (data) => {
            return dispatch(updateAlertModalStatus(data))
        },
        'showGenerateResumeModal': () => {
            return dispatch(showGenerateResumeModal())
        },
        'hideGenerateResumeModal': () => {
            return dispatch(hideGenerateResumeModal())
        },
        "updateSelectedTemplate": (personalInfo) => {
            let { date_of_birth, extracurricular,image,gender} = personalInfo;
            let interest = extracurricular
            interest =  ((interest|| []).filter((item)=>item !==null).map((item)=>item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular': interest,
                    'image' : image,
                    'gender' : gender
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Preview);