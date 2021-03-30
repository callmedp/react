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
            required: false
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
              value: "finance / accounts / investment banking"
            },
            {
              text: "Customer Service / Back Office Operations",
              value: "customer service / back office operations"
            },
            {
              text: "IT - Software",
              value: "it - software"
            },
            {
              text: "Production / Maintenance / Service",
              value: "production / maintenance / service"
            },
            {
              text: "Sales / BD",
              value: "sales / bd"
            },
            {
              text: "IT - Hardware / Networking / Telecom Engineer",
              value: "it - hardware / networking / telecom engineer"
            },
            {
              text: "Engineering Design / Construction",
              value: "engineering design / construction"
            },
            {
              text: "Administration / Front Office / Secretary",
              value: "administration / front office / secretary"
            },
            {
              text: "Marketing / Advertising / MR / PR / Events",
              value: "marketing / advertising / mr / pr / events"
            },
            {
              text: "Quality / Testing (QA-QC)",
              value: "quality / testing (qa-qc)"
            },
            {
              text: "Architecture / Interior Design",
              value: "architecture / interior design"
            },
            {
              text: "Civil Services / Military / Police",
              value: "civil services / military / police"
            },
            {
              text: "Education / Training / Language",
              value: "education / training / language"
            },
            {
              text: "Environment / Health / Safety",
              value: "environment / health / safety"
            },
            {
              text: "Graphic Design / Web Design / Copywriting",
              value: "graphic design / web design / copywriting"
            },
            {
              text: "Hotel / Restaurant",
              value: "hotel / restaurant"
            },
            {
              text: "HR / Recruitment",
              value: "hr / recruitment"
            },
            {
              text: "Journalism / Content / Writing",
              value: "journalism / content / writing"
            },
            {
              text: "Legal / Company Secretary",
              value: "legal / company secretary"
            },
            {
              text: "Management Consulting / Strategy / EA",
              value: "management consulting / strategy / ea"
            },
            {
              text: "Medical / Healthcare",
              value: "medical / healthcare"
            },
            {
              text: "Oil & Gas Engineering / Mining / Geology",
              value: "oil & gas engineering / mining / geology"
            },
            {
              text: "R&D / Product Design",
              value: "r&d / product design"
            },
            {
              text: "Real Estate",
              value: "real estate"
            },
            {
              text: "Retail / Export-Import / Trading",
              value: "retail / export-import / trading"
            },
            {
              text: "SBU Head / CEO / Director / Entrepreneur",
              value: "sbu head / ceo / director / entrepreneur"
            },
            {
              text: "Security / Detective Services",
              value: "security / detective services"
            },
            {
              text: "Statistics / Analytics / Acturial Science",
              value: "statistics / analytics / acturial science"
            },
            {
              text: "Supply Chain / Purchase / Inventory",
              value: "supply chain / purchase / inventory"
            },
            {
              text: "Travel / Aviation / Merchant Navy",
              value: "travel / aviation / merchant navy"
            },
            {
              text: "TV / Film / Radio / Entertainment",
              value: "tv / film / radio / entertainment"
            },
            {
              text: "Other",
              value: "other"
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
            required: false
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
            required: false
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
        placeholder: "Your Skills",
        label: "Your skills",
        inputType: "input",
        validation: {
            required: false
        },
        errorMessage: {
            required: "This field is required"
        },
        children: []
    }
    
}