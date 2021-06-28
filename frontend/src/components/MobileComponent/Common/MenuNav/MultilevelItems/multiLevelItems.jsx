import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom'
import useLearningTracking from 'services/learningTracking';

const MultiLevelItems = props => {
	const {
        item, parentName, setData, sideNavType,
        setType, setOpen, open, usedIn
	} = props
	
	const sendLearningTracking = useLearningTracking();

	const resetNav = (child, index) => {
		setOpen(state => !state);
		setType('menu')
		sendLearningTracking({
			productId: '',
			event: `${props.pageTitle}_multi_level_items_${child.id}`,
			pageTitle: props.pageTitle,
			sectionPlacement: 'header',
			eventCategory: 'multi_level_items',
			eventLabel: '',
			eventAction: 'click',
			algo: '',
			rank: index,
		  })
	}

	const handleLevel = (event, child, index) => {
		event.preventDefault();
		setData([child?.children, child?.name, child?.sideNavType]);
		setType('thirdLevel');
		sendLearningTracking({
			productId: '',
			event: `${props.pageTitle}_multi_level_items_${child.id}`,
			pageTitle: props.pageTitle,
			sectionPlacement: 'header',
			eventCategory: 'multi_level_items',
			eventLabel: '',
			eventAction: 'click',
			algo: '',
			rank: index,
		  })

	}

	return (
		<Menu className={'navigation'} width={'300px'} isOpen={open} onStateChange={state => setOpen(state.isOpen)}>
			<div className="m-guest-section " >
				<React.Fragment>
					<div className="micon-back-menu-white" onClick={() => {!!sideNavType ? setType(sideNavType) : setType('menu')}}></div>
					<div className="media-body">
						<p className="menuText">{parentName}</p>
					</div>
				</React.Fragment>
			</div>
			<div className="m-menu-links">
                {
                    item?.map((child, index) => {
                        return(
                            <React.Fragment key={Math.random()}>
                                {
                                    child?.children?.length ? 
										(
											<a className="menu-item" href='/' onClick={(event)=>handleLevel(event, child, index)} >
												{child.name} 
												<figure className="micon-arrow-menusm ml-auto"></figure>
											</a>
										) : 
										(
											child?.sideNavType === 'courses' ? 
											child?.name === 'Course Catalogue' ? <a className="menu-item" href={child.url} onClick={() => resetNav(child, index)} > {child.name} </a> :
											<Link className="menu-item" to={child.url} onClick={() => resetNav(child, index)}> {child.name} </Link> :
											<a className="menu-item" href={child.url} onClick={() => resetNav(child, index)} > {child.name} </a>
										)
                                }
                            </React.Fragment>
                        )
                    })
                }
			</div>
		</Menu>
	);
}

export default MultiLevelItems;