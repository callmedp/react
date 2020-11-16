import React from "react";
import {BrowserRouter as Router, Route} from "react-router-dom";
import SkillPageContainer from "components/Core/SkillPage/skillPage";


export const RouteWithSubRoutes = route => {
    return(
    <Route
        path={route.path}
        exact={route.exact}
        render={ props => 
            <route.component {...props} routes={route.routes}/>
        }
    />
)};


const AppRouter = () => (
    <Router>
        <div>
            {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </div>
    </Router>
);

export const routes = [
    {
        path : '/skillPage',
        component : SkillPageContainer
    },
    {
        path : '/courses/:func/:skill/:id',
        component : SkillPageContainer
    }
]

export default AppRouter;