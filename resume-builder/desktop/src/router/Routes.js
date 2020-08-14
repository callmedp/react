import Countries from "../components/Countries/index.jsx";
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