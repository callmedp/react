import React, { useState, useEffect} from 'react'

const StickyNav = (props) => {
    const { tabType, setTabType } = props
    const [scrolled, setScrolled] = useState('tab-links');

    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 40 ) {
            setScrolled("tab-links scroll-gradient sticky-top");
        }
        else setScrolled("tab-links");
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
    });

    return (
        <div className={scrolled}>
            <input type="radio" name="tabset" id="tab1" aria-controls="about" />
            <label htmlFor="tab1" className={tabType === 'about' ? 'selected' : ''} onClick={()=>setTabType('about')}>About</label>

            <input type="radio" name="tabset" id="tab2" aria-controls="courses" />
            <label htmlFor="tab2" className={tabType === 'courses' ? 'selected' : ''} onClick={()=>setTabType('courses')}>Courses</label>

            <input type="radio" name="tabset" id="tab3" aria-controls="assessment" />
            <label htmlFor="tab3" className={tabType === 'assessment' ? 'selected' : ''} onClick={()=>setTabType('assessment')}>Assessment</label>
        </div>
    )
}

export default StickyNav;