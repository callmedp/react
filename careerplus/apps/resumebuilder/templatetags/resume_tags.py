from django import template
register = template.Library()

@register.filter
def skillFilterTemplate1(skill):
    skill = skill.split()
    print(skill)
    result= []
    for i in skill[0:3]:
        if len(i) >8 and i!=0:
           result.append(i[0:6] + "..")
        elif len(i) >10 and i==0:
           result.append(i[0:7] + "..")
        else:
            result.append(i)
    skill = ' '.join(result)
    return skill

@register.filter
def mainSkillFilterTemplate1(skill):
    skill = skill.split()
    print(skill)
    result= []
    for i in skill[0:4]:
        if len(i) >12 and i!=0:
           result.append(i[0:10] + "..")
        elif len(i) >13 and i==1:
           result.append(i[0:11] + "..")
        else:
            result.append(i)
    skill = ' '.join(result)
    return skill