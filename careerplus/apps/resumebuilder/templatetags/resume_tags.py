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
    if proficiency == 1:
        return -50
    elif proficiency == 2:
        return -20
    elif proficiency == 3:
        return 10
    elif proficiency == 4:
        return 50
    elif proficiency == 5:
        return 90
    elif proficiency == 6:
        return -65
    elif proficiency == 7:
        return -30
    elif proficiency == 8:
        return 10
    elif proficiency == 9:
        return 50
    elif proficiency == 10:
        return 90
