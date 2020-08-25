import React from 'react';
import { shallow } from 'enzyme';


import Award from './award.jsx';

describe('Award', () => {
    it('should render correctly in "debug" mode', () => {
        const component = shallow(<Award debug />);
        expect(component).toMatchSnapshot();
    });

    it('should render correctly with no props', () => {
        const component = shallow(<Award />);

        expect(component).toMatchSnapshot();
    });
});