import { datepicker as TestDatepicker } from './formFieldRenderer'
import "../../../node_modules/react-datepicker/dist/react-datepicker.css";

import moment from 'moment';
import { shallow, mount, render } from 'enzyme';
import React from 'react';
import toJson from 'enzyme-to-json';




const defaultProps = {
    minDate: moment(0)
}

const Datepicker = (props) =>
    <TestDatepicker  {...defaultProps}
        {...props} />


describe('DatePicker', () => {

    it('render correctly date component', () => {
        const props = {
            meta: {
                touched: null,
                error: null,
                warning: null
            },
            input: {
                value: "10.03.2018"
            }
        }
        const DateInputComponent = render(<Datepicker  {...props} />);
        expect(toJson(DateInputComponent)).toMatchSnapshot();
    });

    it('render date input correctly with null value', () => {
        const props = {
            input: {
                value: null
            },
            meta: {
                touched: null,
                error: null,
                warning: null
            },
        },
            DateInputComponent = mount(<Datepicker {...props} />).find('.Error').children().at(0).getElement();
        expect(DateInputComponent.props.value).toEqual(null);
    });

    it('check the type of value', () => {
        const props = {
            meta: {
                touched: null,
                error: null,
                warning: null
            },
            input: {
                value: "10.03.2018"
            }
        }
        const DateInputComponent = mount(<Datepicker  {...props} />).find('.Error').children().at(0).getElement();
        expect(typeof DateInputComponent.props.value).toBe('string');
    });

    // it('check the onChange callback', () => {
    //     const onChange = jest.fn(),
    //         props = {
    //             input: {
    //                 value: "10.01.2018",
    //                 onChange
    //             },
    //             meta: {
    //                 touched: null,
    //                 error: null,
    //                 warning: null
    //             }
    //         },
    //         DateInputComponent = mount(<Datepicker {...props} />).find('input');
    //     console.log('-----', DateInputComponent.getElements())
    //     DateInputComponent.simulate('change', { target: { value: moment('2018-01-22').format('YYYY-MM-DD').toString() } });
    //     console.log('-----Dat  ', DateInputComponent.getElements());
    //     expect(onChange).toHaveBeenCalledWith('2018-01-21T18:30:00.000Z');
    // });

    it('check DatePicker popup open', () => {

        const
            props = {
                input: {
                    value: null
                },
                meta: {
                    touched: null,
                    error: null,
                    warning: null
                },
            },
            DateComponent = mount(<Datepicker {...props} />),
            dateInput = DateComponent.find("input[type='text']");
            
        dateInput.simulate('click');
        expect(DateComponent.find('.react-datepicker')).toHaveLength(2);
    });
})



