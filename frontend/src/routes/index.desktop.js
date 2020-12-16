import React from "react";
import { BrowserRouter, Route } from "react-router-dom";
import SkillPageContainer from "components/DesktopComponent/Core/SkillPage/skillPage";


export const RouteWithSubRoutes = route => {
    return (
        <Route
            path={route.path}
            exact={route.exact}
            render={props =>
                <route.component {...props} routes={route.routes} />
            }
        />
    )
};


const DesktopAppRouter = (props) => (
    props.isBrowser ? (
        <BrowserRouter>
            <div>
                {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
            </div>
        </BrowserRouter>
    ) : (
            <div>
                {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
            </div>
        )
);

export const routes = [
    {
        path: '/courses/:func/:skill/:id',
        component: SkillPageContainer
    }
]

export default DesktopAppRouter;