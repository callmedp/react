import React from 'react'
import {siteDomain} from "../Utils/domains";
import {
    Redirect
} from 'react-router-dom'

export default class Middleware {

   routeToDisplay(middlewares = [], routeToVisit, directedFrom = '', extra = {}) {
        const mware = {
            privateRoute: (routeToVisit, directedFrom) => this.privateRoute(routeToVisit),
            alreadyLoggedIn: (routeToVisit) => this.alreadyLoggedIn(routeToVisit)
        }

        let ret = null;
        try{
        	for (let i = 0; i < middlewares.length; i++) {
            	ret = mware[middlewares[i]](routeToVisit, directedFrom, extra)
                if (ret.status === false) {
                	break
                }
            }
            return ret.routeObject
        }catch(e){
        	//handle error here
        }

    }

    _getRouteReturn (status, routeObject) {
        return {status, routeObject}
      }

      privateRoute (component, pathname = '/') { 
        return (localStorage.getItem('candidateId') && localStorage.getItem('token')
                ? this._getRouteReturn(true, component)
                : this._getRouteReturn(false,
                  <Redirect to={{
                    pathname: `/resume-builder/`,
                    search: "?login=false",
                    state: { from: pathname }
                  }} />)
        )
      }

      alreadyLoggedIn(component){
          return (
              this._getRouteReturn(true,component)
              )
      }
}