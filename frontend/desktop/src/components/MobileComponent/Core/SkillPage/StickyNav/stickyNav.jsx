import React, {useEffect} from 'react'

const StickyNav = (props) => {
    const [scrolled, setScrolled] = React.useState('');
    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 40 ) {
            setScrolled("sticky-top");
        }
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
    });

    return (
        <>
            <input type="radio" name="tabset" id="tab1" aria-controls="about" defaultChecked />
            <label htmlFor="tab1" className="sticky-top">About</label>

            <input type="radio" name="tabset" id="tab2" aria-controls="courses" />
            <label htmlFor="tab2">Courses</label>

            <input type="radio" name="tabset" id="tab3" aria-controls="assessment" />
            <label htmlFor="tab3">Assessment</label>
        </>
    )
}

export default StickyNav;