import React, {useEffect} from 'react'

const StickyNav = (props) => {
    return (
        <>
            <input type="radio" name="tabset" id="tab1" aria-controls="about" defaultChecked />
            <label htmlFor="tab1" className="sticky-top">About</label>

            <input type="radio" name="tabset" id="tab2" aria-controls="courses" />
            <label htmlFor="tab2" className="sticky-top">Courses</label>

            <input type="radio" name="tabset" id="tab3" aria-controls="assessment" />
            <label htmlFor="tab3" className="sticky-top">Assessment</label>
        </>
    )
}

export default StickyNav;