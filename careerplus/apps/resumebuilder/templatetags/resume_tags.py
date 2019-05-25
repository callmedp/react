from django import template

register = template.Library()


@register.filter
def skillFilterTemplate1(skill):
    skill = skill.split()
    print(skill)
    result = []
    for i in skill[0:3]:
        if len(i) > 8 and i != 0:
            result.append(i[0:6] + "..")
        elif len(i) > 10 and i == 0:
            result.append(i[0:7] + "..")
        else:
            result.append(i)
    skill = ' '.join(result)
    return skill


@register.filter
def mainSkillFilterTemplate1(skill):
    skill = skill.split()
    print(skill)
    result = []
    for i in skill[0:4]:
        if len(i) > 12 and i != 0:
            result.append(i[0:10] + "..")
        elif len(i) > 13 and i == 1:
            result.append(i[0:11] + "..")
        else:
            result.append(i)
    skill = ' '.join(result)
    return skill


@register.filter
def resume1filter(entity_preference):
    exp = entity_preference[2]
    del entity_preference[2], entity_preference[0], entity_preference[3]
    entity_preference.append({'entity_id': 11, 'entity_text': 'Interest', 'active': True})
    entity_preference.append(exp)
    return [x for x in entity_preference if x.get('active')]


@register.filter
def skill_color(proficiency, color):
    if proficiency == 1:
        return '#ebebeb'
    elif proficiency == 2:
        return '#ebebeb'
    elif proficiency == 3:
        return '#ebebeb'
    elif proficiency == 4:
        return '#ebebeb'
    elif proficiency == 5:
        return '#ebebeb'
    elif proficiency == 6:
        return color
    elif proficiency == 7:
        return color
    elif proficiency == 8:
        return color
    elif proficiency == 9:
        return color
    elif proficiency == 10:
        return color


@register.filter
def degree(proficiency):
    proficiency_dict = {
        1: -50,
        2: -20,
        3: 10,
        4: 50,
        5: 90,
        6: -65,
        7: -30,
        8: 10,
        9: 50,
        10: 90
    }
    return proficiency_dict[proficiency]


@register.filter
def background_color_choice(color_code):
    code_dict = {
        1: '#639F59',
        2: '#4D7BA7',
        3: '#D95B5B',
        4: '#000000',
        5: '#C6A828',
        6: '#7C39CA'
    }
    return code_dict[color_code]


@register.filter
def heading_font_size_choice(size):
    heading_size_dict = {
        1: 16,
        2: 17,
        3: 18,
    }
    return heading_size_dict[size]


@register.filter
def sub_heading_font_size(size):
    text_size_dict = {
        1: 16,
        2: 17,
        3: 18
    }
    return text_size_dict[size]


@register.filter
def text_font_size(size):
    text_size_dict = {
        1: 13,
        2: 14,
        3: 15
    }
    return text_size_dict[size]
