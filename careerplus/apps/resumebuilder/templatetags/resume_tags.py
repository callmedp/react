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
        1: 140,
        2: 110,
        3: 70,
        4: 45,
        5: 0,
        6: 145,
        7: 105,
        8: 85,
        9: 30,
        10: 0
    }
    return proficiency_dict.get(proficiency,50)


@register.filter
def background_color_choice(color_code):
    code_dict = {
        1: '#639F59',
        2: '#4D7BA7',
        3: '#D95B5B',
        4: '#000000',
        5: '#C6A828',
        6: '#7C39CA',
    }
    return code_dict.get(color_code,'#639F59')


@register.filter
def heading_font_size_choice(size):
    heading_size_dict = {
        1: 16,
        2: 17,
        3: 18,
    }
    return heading_size_dict.get(size,17)


@register.filter
def sub_heading_font_size(size):
    text_size_dict = {
        1: 16,
        2: 17,
        3: 18
    }
    return text_size_dict.get(size,17)


@register.filter
def text_font_size(size):
    text_size_dict = {
        1: 13,
        2: 14,
        3: 15
    }
    return text_size_dict.get(size,14)


@register.filter
def render_section(choice, template_partial):
    section_choice = {
        1: "profile",
        2: "education",
        3: "experience",
        4: "project",
        5: "skill",
        6: "summary",
        7: "award",
        8: "course",
        9: "language",
        10: "reference",
        11: "interest"
    }
    return template_partial + section_choice[choice] + ".html"

@register.filter
def isDual(index,skill_value):
    if index*2 == skill_value + 1:
        return {'dual':True}
    elif index*2 >skill_value:
        return {'dual':False,'background':"ffffff"}
    else:
        return {'dual':False,'background':"d8d8d8"}

@register.filter
def experiencePosFind(entity_position):
    active_pos =0
    exp_pos = -1
    for i in range(2,len(entity_position)):
        if entity_position[i]['active']:
            active_pos += 1
            if entity_position[i]['entity_id'] == 3:
                exp_pos = active_pos
    return exp_pos
    # for i in entity_position:
    #     if i['entity_id'] == 3:
    #         pos = i['pos']
    #         return pos - 2

@register.filter
def marginSide(experiencePos,pos):
    value = experiencePos - pos
    if value < 0:
        if value % 2 == 0 :
            return 'left'
        return 'right'
    else:
        if value % 2 == 0 :
            return 'right'
        return 'left'

@register.simple_tag
def incrementPos(pos):
    return pos+1

    

