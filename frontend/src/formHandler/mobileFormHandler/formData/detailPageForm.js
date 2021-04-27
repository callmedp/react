export default {
    'name': {
        className: "m-form-control",
        type: "text",
        name: "comment",
        id: "comment",
        placeholder: " ",
        label: "Leave us your message",
        inputType: 'input',
        rows: 3,
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
        
    },
    'email': {
        className: "m-form-control",
        type: "text",
        name: "email",
        id: "email",
        placeholder: " ",
        label: "Email",
        inputType: 'input',
        validation: {
            // required:true,
            pattern:/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        },
        errorMessage: {
            // required: "This field is required",
            pattern: "Email address is invalid!",
            
        }
    },

    'review': {
        className: "m-form-control",
        type: "text",
        name: "review",
        id: "review",
        placeholder: " ",
        label: "Review*",
        inputType: 'input',
        rows: 3,
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
    },
    'title': {
        className: "m-form-control",
        type: "text",
        name: "title",
        id: "title",
        placeholder: " ",
        label: "Title*",
        inputType: 'input',
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
    },
    'mobile': {
        className: "m-form-control",
        type: "number",
        name: "number",
        id: "number",
        placeholder: " ",
        label: "Mobile*",
        inputType: 'input',
        validation: {
            required:true,
            pattern:/^[0-9-]+$/,
            validate : {
                mobLength : value =>  value?.toString().length === 10 
            }
        },
        errorMessage: {
            required: "This field is required",
            pattern: "Mobile number is invalid!",
            mobLength : "Mobile number is invalid!"
        }
    },

    'message': {
        className: "m-form-control",
        type: "text",
        name: "message",
        placeholder: " ",
        id: "message",
        label: "Leave us a message",
        inputType: 'input',
        rows: 3,
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
    },
}