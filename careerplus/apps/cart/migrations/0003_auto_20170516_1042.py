# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_shippingdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingdetail',
            name='country',
            field=models.PositiveIntegerField(choices=[(3, 'Afghanistan'), (15, 'Aland Islands'), (6, 'Albania'), (62, 'Algeria'), (11, 'American Samoa'), (1, 'Andorra'), (8, 'Angola'), (5, 'Anguilla'), (4, 'Antigua and Barbuda'), (10, 'Argentina'), (7, 'Armenia'), (14, 'Aruba'), (13, 'Australia'), (12, 'Austria'), (16, 'Azerbaijan'), (32, 'Bahamas'), (23, 'Bahrain'), (19, 'Bangladesh'), (18, 'Barbados'), (36, 'Belarus'), (20, 'Belgium'), (37, 'Belize'), (25, 'Benin'), (27, 'Bermuda'), (33, 'Bhutan'), (29, 'Bolivia'), (30, 'Bonaire, Saint Eustatius and Saba'), (17, 'Bosnia and Herzegovina'), (35, 'Botswana'), (31, 'Brazil'), (106, 'British Indian Ocean Territory'), (240, 'British Virgin Islands'), (28, 'Brunei'), (22, 'Bulgaria'), (21, 'Burkina Faso'), (24, 'Burundi'), (117, 'Cambodia'), (47, 'Cameroon'), (38, 'Canada'), (52, 'Cape Verde'), (125, 'Cayman Islands'), (41, 'Central African Republic'), (216, 'Chad'), (46, 'Chile'), (48, 'China'), (54, 'Christmas Island'), (39, 'Cocos Islands'), (49, 'Colombia'), (119, 'Comoros'), (45, 'Cook Islands'), (50, 'Costa Rica'), (98, 'Croatia'), (51, 'Cuba'), (53, 'Curacao'), (55, 'Cyprus'), (56, 'Czechia'), (40, 'Democratic Republic of the Congo'), (59, 'Denmark'), (58, 'Djibouti'), (60, 'Dominica'), (61, 'Dominican Republic'), (222, 'East Timor'), (63, 'Ecuador'), (65, 'Egypt'), (211, 'El Salvador'), (88, 'Equatorial Guinea'), (67, 'Eritrea'), (64, 'Estonia'), (69, 'Ethiopia'), (72, 'Falkland Islands'), (74, 'Faroe Islands'), (71, 'Fiji'), (70, 'Finland'), (75, 'France'), (80, 'French Guiana'), (176, 'French Polynesia'), (76, 'Gabon'), (85, 'Gambia'), (79, 'Georgia'), (57, 'Germany'), (82, 'Ghana'), (83, 'Gibraltar'), (89, 'Greece'), (84, 'Greenland'), (78, 'Grenada'), (87, 'Guadeloupe'), (92, 'Guam'), (91, 'Guatemala'), (81, 'Guernsey'), (86, 'Guinea'), (93, 'Guinea-Bissau'), (94, 'Guyana'), (99, 'Haiti'), (97, 'Honduras'), (95, 'Hong Kong'), (100, 'Hungary'), (109, 'Iceland'), (105, 'India'), (101, 'Indonesia'), (108, 'Iran'), (107, 'Iraq'), (102, 'Ireland'), (104, 'Isle of Man'), (103, 'Israel'), (110, 'Italy'), (44, 'Ivory Coast'), (112, 'Jamaica'), (114, 'Japan'), (111, 'Jersey'), (113, 'Jordan'), (126, 'Kazakhstan'), (115, 'Kenya'), (118, 'Kiribati'), (124, 'Kuwait'), (116, 'Kyrgyzstan'), (127, 'Laos'), (136, 'Latvia'), (128, 'Lebanon'), (133, 'Lesotho'), (132, 'Liberia'), (137, 'Libya'), (130, 'Liechtenstein'), (134, 'Lithuania'), (135, 'Luxembourg'), (149, 'Macao'), (145, 'Macedonia'), (143, 'Madagascar'), (157, 'Malawi'), (159, 'Malaysia'), (156, 'Maldives'), (146, 'Mali'), (154, 'Malta'), (144, 'Marshall Islands'), (151, 'Martinique'), (152, 'Mauritania'), (155, 'Mauritius'), (247, 'Mayotte'), (158, 'Mexico'), (73, 'Micronesia'), (140, 'Moldova'), (139, 'Monaco'), (148, 'Mongolia'), (141, 'Montenegro'), (153, 'Montserrat'), (138, 'Morocco'), (160, 'Mozambique'), (147, 'Myanmar'), (161, 'Namibia'), (170, 'Nauru'), (169, 'Nepal'), (167, 'Netherlands'), (252, 'Netherlands Antilles'), (162, 'New Caledonia'), (172, 'New Zealand'), (166, 'Nicaragua'), (163, 'Niger'), (165, 'Nigeria'), (171, 'Niue'), (164, 'Norfolk Island'), (121, 'North Korea'), (150, 'Northern Mariana Islands'), (168, 'Norway'), (173, 'Oman'), (179, 'Pakistan'), (186, 'Palau'), (184, 'Palestinian Territory'), (174, 'Panama'), (177, 'Papua New Guinea'), (187, 'Paraguay'), (175, 'Peru'), (178, 'Philippines'), (182, 'Pitcairn'), (180, 'Poland'), (185, 'Portugal'), (183, 'Puerto Rico'), (188, 'Qatar'), (42, 'Republic of the Congo'), (189, 'Reunion'), (190, 'Romania'), (192, 'Russia'), (193, 'Rwanda'), (26, 'Saint Barthelemy'), (201, 'Saint Helena'), (120, 'Saint Kitts and Nevis'), (129, 'Saint Lucia'), (142, 'Saint Martin'), (181, 'Saint Pierre and Miquelon'), (238, 'Saint Vincent and the Grenadines'), (245, 'Samoa'), (206, 'San Marino'), (210, 'Sao Tome and Principe'), (194, 'Saudi Arabia'), (207, 'Senegal'), (191, 'Serbia'), (251, 'Serbia and Montenegro'), (196, 'Seychelles'), (205, 'Sierra Leone'), (200, 'Singapore'), (212, 'Sint Maarten'), (204, 'Slovakia'), (202, 'Slovenia'), (195, 'Solomon Islands'), (208, 'Somalia'), (248, 'South Africa'), (122, 'South Korea'), (198, 'South Sudan'), (68, 'Spain'), (131, 'Sri Lanka'), (197, 'Sudan'), (209, 'Suriname'), (203, 'Svalbard and Jan Mayen'), (214, 'Swaziland'), (199, 'Sweden'), (43, 'Switzerland'), (213, 'Syria'), (229, 'Taiwan'), (220, 'Tajikistan'), (230, 'Tanzania'), (219, 'Thailand'), (218, 'Togo'), (221, 'Tokelau'), (225, 'Tonga'), (227, 'Trinidad and Tobago'), (224, 'Tunisia'), (226, 'Turkey'), (223, 'Turkmenistan'), (215, 'Turks and Caicos Islands'), (228, 'Tuvalu'), (241, 'U.S. Virgin Islands'), (232, 'Uganda'), (231, 'Ukraine'), (2, 'United Arab Emirates'), (77, 'United Kingdom'), (234, 'United States'), (233, 'United States Minor Outlying Islands'), (235, 'Uruguay'), (236, 'Uzbekistan'), (243, 'Vanuatu'), (237, 'Vatican'), (239, 'Venezuela'), (242, 'Vietnam'), (244, 'Wallis and Futuna'), (66, 'Western Sahara'), (246, 'Yemen'), (249, 'Zambia'), (250, 'Zimbabwe')], default=105),
        ),
        migrations.AlterField(
            model_name='shippingdetail',
            name='country_code',
            field=models.PositiveIntegerField(choices=[(3, '93-(Afghanistan)'), (15, '358-18-(Aland Islands)'), (6, '355-(Albania)'), (62, '213-(Algeria)'), (11, '1-684-(American Samoa)'), (1, '376-(Andorra)'), (8, '244-(Angola)'), (5, '1-264-(Anguilla)'), (4, '1-268-(Antigua and Barbuda)'), (10, '54-(Argentina)'), (7, '374-(Armenia)'), (14, '297-(Aruba)'), (13, '61-(Australia)'), (12, '43-(Austria)'), (16, '994-(Azerbaijan)'), (32, '1-242-(Bahamas)'), (23, '973-(Bahrain)'), (19, '880-(Bangladesh)'), (18, '1-246-(Barbados)'), (36, '375-(Belarus)'), (20, '32-(Belgium)'), (37, '501-(Belize)'), (25, '229-(Benin)'), (27, '1-441-(Bermuda)'), (33, '975-(Bhutan)'), (29, '591-(Bolivia)'), (30, '599-(Bonaire, Saint Eustatius and Saba)'), (17, '387-(Bosnia and Herzegovina)'), (35, '267-(Botswana)'), (31, '55-(Brazil)'), (106, '246-(British Indian Ocean Territory)'), (240, '1-284-(British Virgin Islands)'), (28, '673-(Brunei)'), (22, '359-(Bulgaria)'), (21, '226-(Burkina Faso)'), (24, '257-(Burundi)'), (117, '855-(Cambodia)'), (47, '237-(Cameroon)'), (38, '1-(Canada)'), (52, '238-(Cape Verde)'), (125, '1-345-(Cayman Islands)'), (41, '236-(Central African Republic)'), (216, '235-(Chad)'), (46, '56-(Chile)'), (48, '86-(China)'), (54, '61-(Christmas Island)'), (39, '61-(Cocos Islands)'), (49, '57-(Colombia)'), (119, '269-(Comoros)'), (45, '682-(Cook Islands)'), (50, '506-(Costa Rica)'), (98, '385-(Croatia)'), (51, '53-(Cuba)'), (53, '599-(Curacao)'), (55, '357-(Cyprus)'), (56, '420-(Czechia)'), (40, '243-(Democratic Republic of the Congo)'), (59, '45-(Denmark)'), (58, '253-(Djibouti)'), (60, '1-767-(Dominica)'), (61, '1-809 and 1-829-(Dominican Republic)'), (222, '670-(East Timor)'), (63, '593-(Ecuador)'), (65, '20-(Egypt)'), (211, '503-(El Salvador)'), (88, '240-(Equatorial Guinea)'), (67, '291-(Eritrea)'), (64, '372-(Estonia)'), (69, '251-(Ethiopia)'), (72, '500-(Falkland Islands)'), (74, '298-(Faroe Islands)'), (71, '679-(Fiji)'), (70, '358-(Finland)'), (75, '33-(France)'), (80, '594-(French Guiana)'), (176, '689-(French Polynesia)'), (76, '241-(Gabon)'), (85, '220-(Gambia)'), (79, '995-(Georgia)'), (57, '49-(Germany)'), (82, '233-(Ghana)'), (83, '350-(Gibraltar)'), (89, '30-(Greece)'), (84, '299-(Greenland)'), (78, '1-473-(Grenada)'), (87, '590-(Guadeloupe)'), (92, '1-671-(Guam)'), (91, '502-(Guatemala)'), (81, '44-1481-(Guernsey)'), (86, '224-(Guinea)'), (93, '245-(Guinea-Bissau)'), (94, '592-(Guyana)'), (99, '509-(Haiti)'), (97, '504-(Honduras)'), (95, '852-(Hong Kong)'), (100, '36-(Hungary)'), (109, '354-(Iceland)'), (105, '91-(India)'), (101, '62-(Indonesia)'), (108, '98-(Iran)'), (107, '964-(Iraq)'), (102, '353-(Ireland)'), (104, '44-1624-(Isle of Man)'), (103, '972-(Israel)'), (110, '39-(Italy)'), (44, '225-(Ivory Coast)'), (112, '1-876-(Jamaica)'), (114, '81-(Japan)'), (111, '44-1534-(Jersey)'), (113, '962-(Jordan)'), (126, '7-(Kazakhstan)'), (115, '254-(Kenya)'), (118, '686-(Kiribati)'), (124, '965-(Kuwait)'), (116, '996-(Kyrgyzstan)'), (127, '856-(Laos)'), (136, '371-(Latvia)'), (128, '961-(Lebanon)'), (133, '266-(Lesotho)'), (132, '231-(Liberia)'), (137, '218-(Libya)'), (130, '423-(Liechtenstein)'), (134, '370-(Lithuania)'), (135, '352-(Luxembourg)'), (149, '853-(Macao)'), (145, '389-(Macedonia)'), (143, '261-(Madagascar)'), (157, '265-(Malawi)'), (159, '60-(Malaysia)'), (156, '960-(Maldives)'), (146, '223-(Mali)'), (154, '356-(Malta)'), (144, '692-(Marshall Islands)'), (151, '596-(Martinique)'), (152, '222-(Mauritania)'), (155, '230-(Mauritius)'), (247, '262-(Mayotte)'), (158, '52-(Mexico)'), (73, '691-(Micronesia)'), (140, '373-(Moldova)'), (139, '377-(Monaco)'), (148, '976-(Mongolia)'), (141, '382-(Montenegro)'), (153, '1-664-(Montserrat)'), (138, '212-(Morocco)'), (160, '258-(Mozambique)'), (147, '95-(Myanmar)'), (161, '264-(Namibia)'), (170, '674-(Nauru)'), (169, '977-(Nepal)'), (167, '31-(Netherlands)'), (252, '599-(Netherlands Antilles)'), (162, '687-(New Caledonia)'), (172, '64-(New Zealand)'), (166, '505-(Nicaragua)'), (163, '227-(Niger)'), (165, '234-(Nigeria)'), (171, '683-(Niue)'), (164, '672-(Norfolk Island)'), (121, '850-(North Korea)'), (150, '1-670-(Northern Mariana Islands)'), (168, '47-(Norway)'), (173, '968-(Oman)'), (179, '92-(Pakistan)'), (186, '680-(Palau)'), (184, '970-(Palestinian Territory)'), (174, '507-(Panama)'), (177, '675-(Papua New Guinea)'), (187, '595-(Paraguay)'), (175, '51-(Peru)'), (178, '63-(Philippines)'), (182, '870-(Pitcairn)'), (180, '48-(Poland)'), (185, '351-(Portugal)'), (183, '1-787 and 1-939-(Puerto Rico)'), (188, '974-(Qatar)'), (42, '242-(Republic of the Congo)'), (189, '262-(Reunion)'), (190, '40-(Romania)'), (192, '7-(Russia)'), (193, '250-(Rwanda)'), (26, '590-(Saint Barthelemy)'), (201, '290-(Saint Helena)'), (120, '1-869-(Saint Kitts and Nevis)'), (129, '1-758-(Saint Lucia)'), (142, '590-(Saint Martin)'), (181, '508-(Saint Pierre and Miquelon)'), (238, '1-784-(Saint Vincent and the Grenadines)'), (245, '685-(Samoa)'), (206, '378-(San Marino)'), (210, '239-(Sao Tome and Principe)'), (194, '966-(Saudi Arabia)'), (207, '221-(Senegal)'), (191, '381-(Serbia)'), (251, '381-(Serbia and Montenegro)'), (196, '248-(Seychelles)'), (205, '232-(Sierra Leone)'), (200, '65-(Singapore)'), (212, '599-(Sint Maarten)'), (204, '421-(Slovakia)'), (202, '386-(Slovenia)'), (195, '677-(Solomon Islands)'), (208, '252-(Somalia)'), (248, '27-(South Africa)'), (122, '82-(South Korea)'), (198, '211-(South Sudan)'), (68, '34-(Spain)'), (131, '94-(Sri Lanka)'), (197, '249-(Sudan)'), (209, '597-(Suriname)'), (203, '47-(Svalbard and Jan Mayen)'), (214, '268-(Swaziland)'), (199, '46-(Sweden)'), (43, '41-(Switzerland)'), (213, '963-(Syria)'), (229, '886-(Taiwan)'), (220, '992-(Tajikistan)'), (230, '255-(Tanzania)'), (219, '66-(Thailand)'), (218, '228-(Togo)'), (221, '690-(Tokelau)'), (225, '676-(Tonga)'), (227, '1-868-(Trinidad and Tobago)'), (224, '216-(Tunisia)'), (226, '90-(Turkey)'), (223, '993-(Turkmenistan)'), (215, '1-649-(Turks and Caicos Islands)'), (228, '688-(Tuvalu)'), (241, '1-340-(U.S. Virgin Islands)'), (232, '256-(Uganda)'), (231, '380-(Ukraine)'), (2, '971-(United Arab Emirates)'), (77, '44-(United Kingdom)'), (234, '1-(United States)'), (233, '1-(United States Minor Outlying Islands)'), (235, '598-(Uruguay)'), (236, '998-(Uzbekistan)'), (243, '678-(Vanuatu)'), (237, '379-(Vatican)'), (239, '58-(Venezuela)'), (242, '84-(Vietnam)'), (244, '681-(Wallis and Futuna)'), (66, '212-(Western Sahara)'), (246, '967-(Yemen)'), (249, '260-(Zambia)'), (250, '263-(Zimbabwe)')], default=105, verbose_name='Country Code'),
        ),
    ]
