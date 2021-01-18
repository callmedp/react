import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom'

const MultiLevelItems = props => {
	const {
        item, parentName, setData, sideNavType,
        setType, setOpen, open, usedIn
	} = props
	
	const resetNav = () => {
		setOpen(state => !state);
		setType('menu')
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
                    item?.map((child) => {
                        return(
                            <React.Fragment key={Math.random()}>
                                {
                                    child?.children?.length ? 
										(
											<a className="menu-item" href='/' onClick={(e)=>{e.preventDefault();setData([child?.children, child?.name, child?.sideNavType]); setType('thirdLevel')}} >
												{child.name} 
												<figure className="micon-arrow-menusm ml-auto"></figure>
											</a>
										) : 
										(
											usedIn === 'allCourses' ? 
											child?.name === 'Course Catalogue' ? <a className="menu-item" href={child.url} onClick={resetNav} > {child.name} </a> :
											<Link className="menu-item" to={child.url} onClick={resetNav}> {child.name} </Link> :
											<a className="menu-item" href={child.url} onClick={resetNav} > {child.name} </a>
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