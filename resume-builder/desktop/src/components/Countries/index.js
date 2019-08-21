import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchCountries } from "../../action/countries";
import CountriesItem from './CountriesItem.js';

const m = ({ countries }) => ({ countries });


class Countries extends Component {

  static fetching ({ dispatch }) {
    return [dispatch(fetchCountries())];
  }

  componentDidMount() {
    this.props.fetchCountries();
  }


  render() {
    const { countries: { isFetching, data } } = this.props;

    // if(isFetching) {
    //   return <Loading />
    // }

    return(
      <div className="container">
        <div className="countries-container">
          {data.map((item, i) => <CountriesItem key={i} {...item} />)}
        </div>
      </div>
    );
  }
};


export default connect(m, {fetchCountries})(Countries)
