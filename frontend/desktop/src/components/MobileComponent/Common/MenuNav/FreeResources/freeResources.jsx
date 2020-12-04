import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom'
import { resumeShineSiteDomain } from 'utils/domains';

const FreeResources = props => {
	const { setType, setOpen, open } = props
	const resetNav = () => {
		setOpen(state => !state);
		setType('menu')
	}

	return (
		<Menu className={'navigation'} width={'300px'} isOpen={open} onStateChange={state => setOpen(state.isOpen)}>
			<div className="m-guest-section " >
				<React.Fragment>
					<div className="micon-back-menu-white" onClick={() => setType('menu')}></div>
					<div className="media-body">
						<p className="menuText">Free Resources</p>
					</div>
				</React.Fragment>
			</div>
			<div className="m-menu-links">
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/resume-format/1`} onClick={resetNav} >Resume Formats</a>
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/3/`} onClick={resetNav} >Resignation Letter Formats</a>
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/cover-letter-format/7`} onClick={resetNav} >Cover Letter Formats</a>
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/resume-samples-and-templates/50/`} onClick={resetNav} >Resume Templates</a>
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/linkedin-summary-examples/43`} onClick={resetNav} >LinkedIn Summary Example</a>
                <a className="menu-item" href={`${resumeShineSiteDomain}/cms/relieving-letter-format/58/`} onClick={resetNav} >Relieving Letter</a>
			</div>
		</Menu>
	);
}

export default FreeResources;