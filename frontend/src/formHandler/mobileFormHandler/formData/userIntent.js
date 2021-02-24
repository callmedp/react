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
    'department': {
        className: "form-control",
        type: "text",
        name: "department",
        id: "department",
        label: "Department",
        inputType: 'input',
        validation: {
            required: true
        },
        errorMessage: {
            required: "This field is required"
        },
        children: [
                {
                  text: "Department",
                  value: ""
                },
                {
                  text: "Finance / Accounts / Investment Banking",
                  value: "10007"
                },
                {
                  text: "Customer Service / Back Office Operations",
                  value: "10014"
                },
                {
                  text: "IT - Software",
                  value: "10013"
                },
                {
                  text: "Production / Maintenance / Service",
                  value: "10018"
                },
                {
                  text: "Sales / BD",
                  value: "10033"
                },
                {
                  text: "IT - Hardware / Networking / Telecom Engineer",
                  value: "10012"
                },
                {
                  text: "Engineering Design / Construction",
                  value: "10011"
                },
                {
                  text: "Administration / Front Office / Secretary",
                  value: "10001"
                },
                {
                  text: "Marketing / Advertising / MR / PR / Events",
                  value: "10020"
                },
                {
                  text: "Quality / Testing (QA-QC)",
                  value: "10028"
                },
                {
                  text: "Architecture / Interior Design",
                  value: "10055"
                },
                {
                  text: "Civil Services / Military / Police",
                  value: "10004"
                },
                {
                  text: "Education / Training / Language",
                  value: "10005"
                },
                {
                  text: "Environment / Health / Safety",
                  value: "10050"
                },
                {
                  text: "Graphic Design / Web Design / Copywriting",
                  value: "10056"
                },
                {
                  text: "Hotel / Restaurant",
                  value: "10009"
                },
                {
                  text: "HR / Recruitment",
                  value: "10010"
                },
                {
                  text: "Journalism / Content / Writing",
                  value: "10015"
                },
                {
                  text: "Legal / Company Secretary",
                  value: "10016"
                },
                {
                  text: "Management Consulting / Strategy / EA",
                  value: "10017"
                },
                {
                  text: "Medical / Healthcare",
                  value: "10008"
                },
                {
                  text: "Oil & Gas Engineering / Mining / Geology",
                  value: "10047"
                },
                {
                  text: "R&D / Product Design",
                  value: "10034"
                },
                {
                  text: "Real Estate",
                  value: "10030"
                },
                {
                  text: "Retail / Export-Import / Trading",
                  value: "10042"
                },
                {
                  text: "SBU Head / CEO / Director / Entrepreneur",
                  value: "10040"
                },
                {
                  text: "Security / Detective Services",
                  value: "10035"
                },
                {
                  text: "Statistics / Analytics / Acturial Science",
                  value: "10049"
                },
                {
                  text: "Supply Chain / Purchase / Inventory",
                  value: "10038"
                },
                {
                  text: "Travel / Aviation / Merchant Navy",
                  value: "10003"
                },
                {
                  text: "TV / Film / Radio / Entertainment",
                  value: "10046"
                },
                {
                  text: "Other",
                  value: "10044"
                }
              ]
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