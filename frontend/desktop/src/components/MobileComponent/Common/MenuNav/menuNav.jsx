import React, { useState } from 'react';
import './menuNav.scss'
import DefaultMenuNav from './DefaultMenuNav/defaultMenuNav';
import FreeResources from './FreeResources/freeResources';
import OtherServices from './OtherServices/otherServices';
import ResumeServices from './ResumeServices/resumeServices';
import RecruiterReach from './RecruiterReach/recruiterReach';
 
 
const MenuNav = (props) => {
  const [type, setType] = useState('menu')
  const [open, setOpen] = useState(false)

  switch (type) {
    case 'menu': return < DefaultMenuNav open={open} setOpen={setOpen} setType={setType} />
    case 'freeResources': return <FreeResources open={open} setOpen={setOpen} setType={setType} />
    case 'otherServices': return < OtherServices open={open} setOpen={setOpen} setType={setType} />
    case 'resumeServices': return <ResumeServices open={open} setOpen={setOpen} setType={setType} />
    case 'recruiterReach': return <RecruiterReach open={open} setOpen={setOpen} setType={setType} />
    default: return < DefaultMenuNav setType={setType} />
  }
}

export default MenuNav;