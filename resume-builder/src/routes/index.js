import React from "react";
import {BrowserRouter as Router, Route} from "react-router-dom";
import EditContainer from '../components/Core/Editor/Edit/edit.jsx';
import PreviewContainer from '../components/Core/Editor/Preview/preview.jsx';
import HomeContainer from '../components/Core/Home/home.jsx';

export const RouteWithSubRoutes = route => (
    <Route
        path={route.path}
        exact={route.exact}
        render={props => (
            // pass the sub-routes down to keep nesting
            <route.component {...props} routes={route.routes}/>
        )}
    />
);


const AppRouter = () => (
    <Router>
        <div>
            {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </div>
    </Router>
);

const routes = [
    {
        path: '/resume-builder',
        component: HomeContainer,
        exact: true
    },
    {
        path: '/resume-builder/edit/',
        component: EditContainer
    },
    {
        path: '/resume-builder/preview',
        component: PreviewContainer
    }

]

export default AppRouter;