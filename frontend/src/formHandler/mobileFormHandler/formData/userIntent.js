export default {
    'job': {
        className: "form-control",
        type: "text",
        name: "job",
        id: "job",
        placeholder: " ",
        label: "Current job title",
        inputType: 'input',
        validation: {
            required: true,
        },
        errorMessage: {
            required: "This field is required"
        }
    },
    'experience': {
        name: 'experience',
        inputType: 'select',
        children: [
            {
                text: "Total Experience",
                value: ""
            },
            {
                text: "1 Yr",
                value: "1 Yr",
            },
            {
                text: "2 Yrs",
                value: "2 Yrs",
            },
            {
                text: "3 Yrs",
                value: "3 Yrs",
            },
            {
                text: "4 Yrs",
                value: "4 Yrs",
            },
            {
                text: "5 Yrs",
                value: "5 Yrs",
            },
            {
                text: "6 Yrs",
                value: "6 Yrs",
            },
            {
                text: "7 Yrs",
                value: "7 Yrs",
            },
            {
                text: "8 Yrs",
                value: "8 Yrs",
            },
            {
                text: "9 Yrs",
                value: "9 Yrs",
            },
            {
                text: "10 Yrs",
                value: "10 Yrs",
            },
            {
                text: "11 Yrs",
                value: "11 Yrs",
            },
            {
                text: "12 Yrs",
                value: "12 Yrs",
            },
            {
                text: "13 Yrs",
                value: "13 Yrs",
            },
            {
                text: "14 Yrs",
                value: "14 Yrs",
            },
            {
                text: "15 Yrs",
                value: "15 Yrs",
            },
            {
                text: "16 Yrs",
                value: "16 Yrs",
            },
            {
                text: "17+ Yrs",
                value: "17+ Yrs",
            },
        ],
        validation: {
            required: true
        },
        errorMessage: {
            required: "This field is required"
        }
    },
    'location': {
        className: "form-control",
        name: "location",
        type: "text",
        placeholder: " ",
        label: "Preferred location",
        inputType: "input",
        validation: {
            required: true
        },
        errorMessage: {
            required: "This field is required"
        }
    },
    'skills': {
        className: "form-control",
        name: "skills",
        id: "skills",
        type: "text",
        placeholder: "Keyword Research",
        label: "Your skills",
        inputType: "input",
        validation: {
            required: true
        },
        errorMessage: {
            required: "This field is required"
        },
        children: []
    }
    
}