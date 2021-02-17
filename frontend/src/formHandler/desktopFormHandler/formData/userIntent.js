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
                text: "1-2",
                value: "1-2",
            },
            {
                text: "3-5",
                value: "3-5",
            },
            {
                text: "6+",
                value: "6+"
            }
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
        type: "text",
        placeholder: " ",
        label: "Your skills",
        inputType: "input",
        validation: {
            required: true
        },
        errorMessage: {
            required: "This field is required"
        }
    }
    
}