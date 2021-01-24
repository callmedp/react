import React from 'react';
import Card from 'react-bootstrap/Card';
import Accordion from 'react-bootstrap/Accordion';
import { MyGA } from '../../../../utils/ga.tracking.js';
const regex = /(<([^>]+)>)/ig;

const FaqAccordion = (item, index) => {
    return (
        <Card key={index.toString() + item.heading} itemScope itemProp="mainEntity" 
        itemType="https://schema.org/Question" >
            <Accordion.Toggle as={Card.Header} eventKey={index === 0 ? '0' : index} >
                <p dangerouslySetInnerHTML={{__html : item.heading}} onClick={() => MyGA.SendEvent('FAQs','ln_FAQ_click', 'ln_down_arrow_click', 'ln_'+item.heading.replace(regex, ''),'', false, true) }></p>
                <meta itemProp="name" content={item.heading} />
            </Accordion.Toggle>
            <Accordion.Collapse eventKey={index === 0 ? '0' : index} itemProp="acceptedAnswer" itemScope 
                            itemType="https://schema.org/Answer">
                <Card.Body itemProp="text" dangerouslySetInnerHTML={{ __html: item.content }}>
                </Card.Body>
            </Accordion.Collapse>
        </Card>
    )
}

export default FaqAccordion;