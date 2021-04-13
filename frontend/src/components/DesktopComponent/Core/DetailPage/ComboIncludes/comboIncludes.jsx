import React from 'react';
import './comboIncludes.scss';

const ComboIncludes = (props) => {
    const {combo_list} = props;
    return (
        <div className="combo-includes mt-20">
            <h2 className="heading2">Combo includes</h2>
            <ul className="combo-includes__list">
                {
                    combo_list?.map((combData, indx) => {
                        return (
                            <li key={indx}>
                                <a href={`${combData.url}`}>{combData.heading}</a>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}

export default ComboIncludes;