export default {
    'name': {
        className: "input_field",
        type: "text",
        name: "name",
        id: "name",
        label: "Name*",
        inputType: 'input',
        validation: {
            required:true,
        },
        errorMessage: {
            required: "This field is required",
        }
        
    },
    'email': {
        className: "input_field",
        type: "text",
        name: "email",
        id: "email",
        label: "Email*",
        inputType: 'input',
        validation: {
            required:true,
            pattern:/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        },
        errorMessage: {
            required: "This field is required",
            pattern: "Email address is invalid!",
            
        }
    },
    'mobile': {
        className: "input_field",
        type: "number",
        name: "cell_phone",
        id: "cell_phone",
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
    'country_code': {
        name: "country_code",
        inputType: 'select',
        children: [
            {
                text:"India",
                value:"91",
                
            },   
            {
                text:"Israel",
                value:"972",
            },
            {
                text:"Afghanistan",
                value:"93",
            
            },
            {
                text:"Albania",
                value:"355",
            
            },
            {
                text:"Algeria",
                value:"213",
            
            },
            {
                text:"AmericanSamoa",
                value:"1 684",
            
            },
            {
                text:"Andorra",
                value:"376",
            
            },
            {
                text:"Angola",
                value:"244",
            
            },
            {
                text:"Anguilla",
                value:"1 264"
            
            },
            {
                text:"Antigua and Barbuda",
                value:"1268",
            
            },
            {
                text:"Argentina",
                value:"54",
            
            },
            {
                text:"Armenia",
                value:"374",
            
            },
            {
                text:"Aruba",
                value:"297",
            
            },
            {
                text:"Australia",
                value:"61",
            
            },
            {
                text:"Austria",
                value:"43",
            
            },
            {
                text:"Azerbaijan",
                value:"994",
                    
            },
            {
                text:"Bahamas",
                value:"1 242",
                    
            },
            {
                text:"Bahrain",
                value:"973",
                  
            },
            {
                text:"Bangladesh",
                value:"880",
                    
            },
            {
                text:"Barbados",
                value:"1 246",
                    
            },
            {
                text:"Belarus",
                value:"375",
                   
            },
            {
                text:"Belgium",
                value:"32",
                    
            },
            {
                text:"Belize",
                value:"501",
                 
            },
            {
                text:"Benin",
                value:"229",
                
            },
            {
                text:"Bermuda",
                value:"1 441",
                
            
            },
            {
                text:"Bhutan",
                value:"975",
                
            
            },
            {
                text:"Bosnia and Herzegovina",
                value:"387",
                   
            },
            {
                text:"Botswana",
                value:"267",
                
            },
            {
                text:"Brazil",
                value:"55",
                 
            },
            {
                text:"British Indian Ocean Territory",
                value:"246",
            },
            {
                text:"Bulgaria",
                value:"359",
                
            },
            {
                text:"Burkina Faso",
                value:"226",
                   
            },
            {
                text:"Burundi",
                value:"257",
                    
            },
            {
                text:"Cambodia",
                value:"855",
                
            
            },
            {
                text:"Cameroon",
                value:"237",
                    
            },
            {
                text:"Canada",
                value:"1",
                
            
            },
            {
                text:"Cape Verde",
                value:"238",
                
            
            },
            {
                text:"Cayman Islands",
                value:" 345",
                    
            },
            {
                text:"Central African Republic",
                value:"236",
                    
            },
            {
                text:"Chad",
                value:"235",
                    
            },
            {
                text:"Chile",
                value:"56",
                   
            },
            {
                text:"China",
                value:"86",
                    
            },
            {
                text:"Christmas Island",
                value:"61",
                   
            },
            {
                text:"Colombia",
                value:"57",
                
            
            },
            {
                text:"Comoros",
                value:"269",
                    
            },
            {
                text:"Congo",
                value:"242",
                    
            },
            {
                text:"Cook Islands",
                value:"682",
                   
            },
            {
                text:"Costa Rica",
                value:"506",
                  
            },
            {
                text:"Croatia",
                value:"385",
                 
            },
            {
                text:"Cuba",
                value:"53",
                
            },
            {
                text:"Cyprus",
                value:"537",
                    
            },
            {
                text:"Czech Republic",
                value:"420",
                    
            },
            {
                text:"Denmark",
                value:"45",
                    
            },
            {
                text:"Djibouti",
                value:"253",
                    
            },
            {
                text:"Dominica",
                value:"1 767",
                    
            },
            {
                text:"Dominican Republic",
                value:"1 849",
                   
            },
            {
                text:"Ecuador",
                value:"593",
                   
            },
            {
                text:"Egypt",
                value:"20",
                   
            },
            {
                text:"El Salvador",
                value:"503",
                   
            },
            {
                text:"Equatorial Guinea",
                value:"240",
                   
            },
            {
                text:"Eritrea",
                value:"291",
                  
            },
            {
                text:"Estonia",
                value:"372",
                
            },
            {
                text:"Ethiopia",
                value:"251",
                    
            },
            {
                text:"Faroe Islands",
                value:"298",
                   
            },
            {
                text:"Fiji",
                value:"679",
                    
            },
            {
                text:"Finland",
                value:"358",
                    
            },
            {
                text:"France",
                value:"33",
                    
            },
            {
                text:"French Guiana",
                value:"594",
                   
            },
            {
                text:"French Polynesia",
                value:"689",
                  
            },
            {
                text:"Gabon",
                value:"241",
                
            
            },
            {
                text:"Gambia",
                value:"220",
                
            },
            {
                text:"Georgia",
                value:"995",
                
            },
            {
                text:"Germany",
                value:"49",
                
            },
            {
                text:"Ghana",
                value:"233",
                
            },
            {
                text:"Gibraltar",
                value:"350",
            
            },
            {
                text:"Greece",
                value:"30",
                
            },
            {
                text:"Greenland",
                value:"299",
                
            },
            {
                text:"Grenada",
                value:"1 473",
                
            },
            {
                text:"Guadeloupe",
                value:"590",
            
            },
            {
                text:"Guam",
                value:"1 671",
            
            },
            {
                text:"Guatemala",
                value:"502",
            
            },
            {
                text:"Guinea",
                value:"224",
            
            },
            {
                text:"Guinea-Bissau",
                value:"245",
             
            },
            {
                text:"Guyana",
                value:"595",
            },
            {
                text:"Haiti",
                value:"509",
                
            },
            {
                text:"Honduras",
                value:"504",
                
            },
            {
                text:"Hungary",
                value:"36",
               
            },
            {
                text:"Iceland",
                value:"354",
                
            },
            {
                text:"Indonesia",
                value:"62",
              
            },
            {
                text:"Iraq",
                value:"964",
               
            },
            {
                text:"Ireland",
                value:"353",
              
            },
            {
                text:"Israel",
                value:"972",
              
            },
            {
                text:"Italy",
                value:"39",
                
            },
            {
                text:"Jamaica",
                value:"1 876",
              
            },
            {
                text:"Japan",
                value:"81",
            
            },
            {
                text:"Jordan",
                value:"962",
                
            },
            {
                text:"Kazakhstan",
                value:"7 7",
                
            },
            {
                text:"Kenya",
                value:"254",
                
            },
            {
                text:"Kiribati",
                value:"686",
                
            },
            {
                text:"Kuwait",
                value:"965",
               
            },
            {
                text:"Kyrgyzstan",
                value:"996",
             
            },
            {
                text:"Latvia",
                value:"371",
               
            },
            {
                text:"Lebanon",
                value:"961",
            
            },
            {
                text:"Lesotho",
                value:"266",
            
            },
            {
                text:"Liberia",
                value:"231",
            
            },
            {
                text:"Liechtenstein",
                value:"423",
            
            },
            {
                text:"Lithuania",
                value:"370",
            
            },
            {
                text:"Luxembourg",
                value:"352",
            
            },
            {
                text:"Madagascar",
                value:"261",
             
            },
            {
                text:"Malawi",
                value:"265",
               
            },
            {
                text:"Malaysia",
                value:"60",
                
            },
            {
                text:"Maldives",
                value:"960",
             
            },
            {
                text:"Mali",
                value:"223",
               
            },
            {
                text:"Malta",
                value:"356",
                
            },
            {
                text:"Marshall Islands",
                value:"692",
            
            },
            {
                text:"Martinique",
                value:"596",
              
            },
            {
                text:"Mauritania",
                value:"222",
                
            },
            {
                text:"Mauritius",
                value:"230",
                
            },
            {
                text:"Mayotte",
                value:"262",
               
            },
            {
                text:"Mexico",
                value:"52",
             
            },
            {
                text:"Monaco",
                value:"377",
                
            },
            {
                text:"Mongolia",
                value:"976",
                
            },
            {
                text:"Montenegro",
                value:"382",
               
            },
            {
                text:"Montserrat",
                value:"1664",
                
            },
            {
                text:"Morocco",
                value:"212",
              
            },
            {
                text:"Myanmar",
                value:"95",
                
            },
            {
                text:"Namibia",
                value:"264",
              
            },
            {
                text:"Nauru",
                value:"674",
               
            },
            {
                text:"Nepal",
                value:"977",
               
            },
            {
                text:"Netherlands",
                value:"31",
             
            },
            {
                text:"Netherlands Antilles",
                value:"599",
               
            },
            {
                text:"New Caledonia",
                value:"687",
            
            },
            {
                text:"New Zealand",
                value:"64",
                
            },
            {
                text:"Nicaragua",
                value:"505",
              
            },
            {
                text:"Niger",
                value:"227",
               
            },
            {
                text:"Nigeria",
                value:"234",    
            },
            {
                text:"Niue",
                value:"683",
            
            },
            {
                text:"Norfolk Island",
                value:"672",
             
            },
            {
                text:"Northern Mariana Islands",
                value:"1 670",
               
            },
            {
                text:"Norway",
                value:"47",
            
            },
            {
                text:"Oman",
                value:"968",
              
            },
            {
                text:"Pakistan",
                value:"92",
               
            },
            {
                text:"Palau",
                value:"680",
                
            },
            {
                text:"Panama",
                value:"507",
            
            },
            {
                text:"Papua New Guinea",
                value:"675",
               
            },
            {
                text:"Paraguay",
                value:"595",
               
            },
            {
                text:"Peru",
                value:"51",
               
            },
            {
                text:"Philippines",
                value:"63",
               
            },
            {
                text:"Poland",
                value:"48",
            
            },
            {
                text:"Portugal",
                value:"351",
            
            },
            {
                text:"Puerto Rico",
                value:"1 939",
               
            },
            {
                text:"Qatar",
                value:"974",
             
            },
            {
                text:"Romania",
                value:"40",
               
            },
            {
                text:"Rwanda",
                value:"250",
            
            },
            {
                text:"Samoa",
                value:"685",
              
            },
            {
                text:"San Marino",
                value:"378",
             
            },
            {
                text:"Saudi Arabia",
                value:"966",
              
            },
            {
                text:"Senegal",
                value:"221",
              
            },
            {
                text:"Serbia",
                value:"381",
             
            },
            {
                text:"Seychelles",
                value:"248",
              
            },
            {
                text:"Sierra Leone",
                value:"232",
               
            },
            {
                text:"Singapore",
                value:"65",
                
            },
            {
                text:"Slovakia",
                value:"421",
            
            },
            {
                text:"Slovenia",
                value:"386",
               
            },
            {
                text:"Solomon Islands",
                value:"677",
               
            },
            {
                text:"South Africa",
                value:"27",
              
            },
            {
                text:"South Georgia and the South Sandwich Islands",
                value:"500",
               
            },
            {
                text:"Spain",
                value:"34",
            
            },
            {
                text:"Sri Lanka",
                value:"94",
            
            },
            {
                text:"Sudan",
                value:"249",
               
            },
            {
                text:"Suriname",
                value:"597",
                
            },
            {
                text:"Swaziland",
                value:"268",
            
            },
            {
                text:"Sweden",
                value:"46",
               
            },
            {
                text:"Switzerland",
                value:"41",
              
            },
            {
                text:"Tajikistan",
                value:"992",
               
            },
            {
                text:"Thailand",
                value:"66",
                
            },
            {
                text:"Togo",
                value:"228",
              
            },
            {
                text:"Tokelau",
                value:"690",
               
            },
            {
                text:"Tonga",
                value:"676",
            
            },
            {
                text:"Trinidad and Tobago",
                value:"1 868",
               
            },
            {
                text:"Tunisia",
                value:"216",
                
            },
            {
                text:"Turkey",
                value:"90",
                
            },
            {
                text:"Turkmenistan",
                value:"993",
            
            },
            {
                text:"Turks and Caicos Islands",
                value:"1 649",
               
            },
            {
                text:"Tuvalu",
                value:"688",
             
            },
            {
                text:"Uganda",
                value:"256",
            
            },
            {
                text:"Ukraine",
                value:"380",
              
            },
            {
                text:"United Arab Emirates",
                value:"971",
                
            },
            {
                text:"United Kingdom",
                value:"44",
              
            },
            {
                text:"United States",
                value:"1",
               
            },
            {
                text:"Uruguay",
                value:"598",
               
            },
            {
                text:"Uzbekistan",
                value:"998",
                
            },
            {
                text:"Vanuatu",
                value:"678",
               
            },
            {
                text:"Wallis and Futuna",
                value:"681",
             
            },
            {
                text:"Yemen",
                value:"967",
               
            },
            {
                text:"Zambia",
                value:"260",
                
            },
            {
                text:"Zimbabwe",
                value:"263",
               
            },
            
            {
                text:"Bolivia, Plurinational State of",
                value:"591",
                
            },
            {
                text:"Brunei Darussalam",
                value:"673",
               
            },
            {
                text:"Cocos (Keeling) Islands",
                value:"61",
              
            },
            {
                text:"Congo, The Democratic Republic of the",
                value:"243",
               
            },
            {
                text:"Cote d'Ivoire",
                value:"225",
               
            },
            {
                text:"Falkland Islands (Malvinas)",
                value:"500",
                
            },
            {
                text:"Guernsey",
                value:"44",
            
            },
            {
                text:"Holy See (Vatican City State)",
                value:"379",
              
            },
            {
                text:"Hong Kong",
                value:"852",
             
            },
            {
                text:"Iran, Islamic Republic of",
                value:"98",
              
            },
            {
                text:"Isle of Man",
                value:"44",
             
            },
            {
                text:"Jersey",
                value:"44",
              
            },
            {
                text:"Korea, Democratic People's Republic of",
                value:"850",
            },
            {
                text:"Korea, Republic of",
                value:"82",
               
            },
            {
                text:"Lao People's Democratic Republic",
                value:"856",
                
            },
            {
                text:"Libyan Arab Jamahiriya",
                value:"218",
             
            },
            {
                text:"Macao",
                value:"853",
               
            },
            {
                text:"Macedonia, The Former Yugoslav Republic of",
                value:"389",
             
            },
            {
                text:"Micronesia, Federated States of",
                value:"691",
            
            },
            {
                text:"Moldova, Republic of",
                value:"373",
               
            },
            {
                text:"Mozambique",
                value:"258",
               
            },
            {
                text:"Palestinian Territory, Occupied",
                value:"970",
              
            },
            {
                text:"Pitcairn",
                value:"872",
               
            },
            {
                text:"Réunion",
                value:"262",
              
            },
            {
                text:"Russia",
                value:"7",
            },
            {
                text:"Saint Barthélemy",
                value:"590",
            },
            {
                text:"Saint Helena, Ascension and Tristan Da Cunha",
                value:"290",
                
            },
            {
                text:"Saint Kitts and Nevis",
                value:"1 869",
                
            },
            {
                text:"Saint Lucia",
                value:"1 758",
                
            },
            {
                text:"Saint Martin",
                value:"590",
               
            },
            {
                text:"Saint Pierre and Miquelon",
                value:"508",
                
            },
            {
                text:"Saint Vincent and the Grenadines",
                value:"1 784",
                
            },
            {
                text:"Sao Tome and Principe",
                value:"239",
               
            },
            {
                text:"Somalia",
                value:"252",
                
            },
            {
                text:"Svalbard and Jan Mayen",
                value:"47",
            
            
            },
            {
                text:"Syrian Arab Republic",
                value:"963",
            
            },
            {
                text:"Taiwan, Province of China",
                value:"886",
            
            },
            {
                text:"Tanzania, United Republic of",
                value:"255",
            
            },
            {
                text:"Timor-Leste",
                value:"670",
            
            },
            {
                text:"Venezuela, Bolivarian Republic of",
                value:"58",
            
            },
            {
                text:"Viet Nam",
                value:"84",
            
            },
            {
                text:"Virgin Islands, British",
                value:"1 284",
            
            },
            {
                text:"Virgin Islands, U.S.",
                value:"1 340",
            
            }
        ]
    }
}