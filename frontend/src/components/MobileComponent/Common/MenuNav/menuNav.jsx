import React, { useState } from 'react';
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

  switch (type) {
    case 'menu': return < DefaultMenuNav open={open} setOpen={setOpen} setType={setType} />
    case 'freeResources': return <FreeResources open={open} setOpen={setOpen} setType={setType} item={freeResourcesList} parentName="Free Resources" setData={setData}/>
    case 'jobAssistanceServices': return <ResumeServices open={open} setOpen={setOpen} setType={setType} item={jobAssistanceList} parentName="Resume Services"/>
    case 'allCourses': return <AllCourses open={open} setOpen={setOpen} setType={setType} item={categoryList} parentName="All Courses" setData={setData}/>
    case 'thirdLevel': return <ThirdLevel open={open} setOpen={setOpen} setType={setType} item={data[0]} parentName={data[1]} sideNavType={data[2]}/>
    default: return < DefaultMenuNav setType={setType} />
  }
}

export default MenuNav;