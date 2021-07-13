import React, { useState, useEffect } from 'react';
import './menuNav.scss'
import DefaultMenuNav from './DefaultMenuNav/defaultMenuNav';
import FreeResources from './MultilevelItems/multiLevelItems';
import ResumeServices from './MultilevelItems/multiLevelItems';
import AllCourses from './MultilevelItems/multiLevelItems';
import ThirdLevel from './MultilevelItems/multiLevelItems';
import { freeResourcesList, jobAssistanceList, categoryList } from 'utils/constants';
 
 
const MenuNav = (props) => {
  const [type, setType] = useState('menu')
  const [data, setData] = useState([])
  const [open, setOpen] = useState(false)
  const { pageTitle } = props;

  switch (type) {
    case 'menu': return < DefaultMenuNav pageTitle = {pageTitle} open={open} setOpen={setOpen} setType={setType} />
    case 'freeResources': return <FreeResources pageTitle = {pageTitle} open={open} setOpen={setOpen} setType={setType} item={freeResourcesList} parentName="Free Resources" setData={setData}/>
    case 'jobAssistanceServices': return <ResumeServices pageTitle = {pageTitle} open={open} setOpen={setOpen} setType={setType} item={jobAssistanceList} parentName="Resume Services"/>
    case 'allCourses': return <AllCourses pageTitle = {pageTitle} open={open} setOpen={setOpen} setType={setType} item={categoryList} parentName="All Courses" setData={setData}/>
    case 'thirdLevel': return <ThirdLevel pageTitle = {pageTitle} open={open} setOpen={setOpen} setType={setType} item={data[0]} parentName={data[1]} sideNavType={data[2]}/>
    default: return < DefaultMenuNav pageTitle = {pageTitle} setType={setType} />
  }
}

export default MenuNav;