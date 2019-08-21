import Countries from "../components/Countries/index.js";
import Country from "../components/Country/index.js";


export default [
  {
    component: Countries,
    path: '/',
    exact: true
  },
  {
    component: Country,
    path: '/:name'
  }
];