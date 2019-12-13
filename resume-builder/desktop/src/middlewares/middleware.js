import React from 'react'
import { siteDomain } from "../Utils/domains";
import {
  Redirect
} from 'react-router-dom'

export default class Middleware {

  routeToDisplay(middlewares = [], routeToVisit, directedFrom = '', extra = {}) {
    const mware = {
      privateRoute: (routeToVisit, directedFrom) => this.privateRoute(routeToVisit, directedFrom),
      alreadyLoggedIn: (routeToVisit) => this.alreadyLoggedIn(routeToVisit)
    }

    let ret = null;
    try {
      for (let i = 0; i < middlewares.length; i++) {
        ret = mware[middlewares[i]](routeToVisit, directedFrom, extra)
        if (ret.status === false) {
          break
        }
      }
      return ret.routeObject
    } catch (e) {
      //handle error here
    }

  }

  _getRouteReturn(status, routeObject) {
    return { status, routeObject }
  }

  privateRoute(component, pathname = '/') {
    let buyPath = false;
    const componentPathname = component && component.props && component.props.location && component.props.location.pathname || ''

    if (componentPathname === '/resume-builder/buy') {
      buyPath = true;
    }
    return (localStorage.getItem('candidateId') && localStorage.getItem('token')
      ? localStorage.getItem('selected_template') ?
        (buyPath ?
          (localStorage.getItem('orderAvailable') ?
            this._getRouteReturn(false, <Redirect to={{
              pathname: '/resume-builder',
            }} />) :
            this._getRouteReturn(true, component)
          )
          :
          this._getRouteReturn(true, component)
        )
        :
        this._getRouteReturn(false,
          <Redirect to={{
            pathname: `/resume-builder/`,
            search: "?template=false",
            state: { from: pathname }
          }} />)
      : this._getRouteReturn(false,
        <Redirect to={{
          pathname: `/resume-builder/`,
          search: "?login=false",
          state: { from: pathname }
        }} />)
    )
  }

  alreadyLoggedIn(component) {
    return (
      this._getRouteReturn(true, component)
    )
  }
}