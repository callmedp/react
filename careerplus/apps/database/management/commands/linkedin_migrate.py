# import MySQLdb
# import json
# import pandas as pd
# import numpy as np
# from decimal import Decimal
# from django.utils import timezone
# from datetime import datetime
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from django.db import IntegrityError, transaction
# from django.contrib.contenttypes.models import ContentType
# from database.models import CPUser
# from shop.models import Product

# class Command(BaseCommand):
#     help = ('Get User Database from old Careerplus')

#     def handle(self, *args, **options):
#         db_settings=settings.DATABASES.get('oldDB')
#         db_host = db_settings.get('HOST')
#         if db_host is '':
#             db_host = "localhost"
#         db_name = db_settings.get('NAME')
#         db_pwd = db_settings.get('PASSWORD')
#         db_user = db_settings.get('USER')
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         db2_settings=settings.DATABASES.get('default')
#         db2_host = db2_settings.get('HOST')
#         if db2_host is '':
#             db2_host = "localhost"
#         db2_name = db2_settings.get('NAME')
#         db2_pwd = db2_settings.get('PASSWORD')
#         db2_user = db2_settings.get('USER')
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         sql = """
#                 SELECT qwiz_quizresponse.id, qwiz_quizresponse.oi_id, qwiz_quizresponse.submitted, qwiz_quizresponse.created_on, 
#                 qwiz_quizresponse.modified_on, qwiz_answer.id as answer, qwiz_answer.text, 
#                 qwiz_answer.question_id 
#                 FROM qwiz_quizresponse 
#                 LEFT OUTER JOIN qwiz_answer 
#                 ON ( qwiz_quizresponse.id = qwiz_answer.quiz_response_id ) 
#                 WHERE qwiz_quizresponse.oi_id IS NOT NULL
#             """
#         question_dict = {
#             1: 'According to you what does it take for a business to survive and find success?',
#             2: 'What kind of results can a person expect from working with you?',
#             3: 'What sets you apart from others? Which of your personal attributes have been most beneficial to you in your career? Explain why.',
#             4: 'Name 1 or 2 defining accomplishments. Think of events or projects that shaped your career path and make you proud. What was the impact of these accomplishments on you, your business, and your customers?',
#             5: 'What is your goal moving forward?  What do you hope to achieve?'
#             }
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         quiz_df = pd.read_sql(sql, con=db)
#         quiz_df = quiz_df.groupby(['id', 'created_on', 'modified_on', 'oi_id', 'submitted']).apply(lambda x: dict(zip(x['question_id'], x['text']))).reset_index().rename(columns={0:"answerset"})
#         new_order_item_df = pd.read_sql(
#             'SELECT order_orderitem.id as oi_new_id, order_orderitem.coi_id as oi_id FROM order_orderitem ;',con=db2)
#         quiz_df = pd.merge(quiz_df, new_order_item_df, how='left', on='oi_id')
#         quiz_df = quiz_df[~quiz_df.oi_new_id.isnull()]
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Mysql order select done')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         cursor = db2.cursor()

#         update_values = []
#         update_sql = """
#                 INSERT INTO quizs_quizresponse 
#                 (created_on, modified_on, oi_id, submitted, question1, anser1,
#                 question2, anser2, question3, anser3, question4, anser4,
#                 question5, anser5) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                
#                 """
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Qwiz Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in quiz_df.iterrows():
#             if row['oi_new_id'] and row['oi_new_id'] == row['oi_new_id']:
#                 answer_dict = row['answerset']
#                 answer1 = answer_dict.get(1,'')
#                 answer2 = answer_dict.get(2,'')
#                 answer3 = answer_dict.get(3,'')
#                 answer4 = answer_dict.get(4,'')
#                 answer5 = answer_dict.get(5,'')
#                 data_tup = (
#                     str(row['created_on']) if row['created_on'] == row['created_on'] else None,
#                     str(row['modified_on']) if row['modified_on'] == row['modified_on'] else None,
#                     row['oi_new_id'], 
#                     row['submitted'],
#                     question_dict[1],
#                     answer1,
#                     question_dict[2],
#                     answer2,
#                     question_dict[3],
#                     answer3,
#                     question_dict[4],
#                     answer4,
#                     question_dict[5],
#                     answer5
#                 )
                
#                 update_values.append(data_tup)    
#             if len(update_values) > 1000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 cursor.executemany(update_sql, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql, update_values)
#             update_values = []
        
#         del quiz_df
        
#         sql2 = """
#             SELECT linkedin_draft.id, linkedin_draft.candidate_name, linkedin_draft.headline, 
#             linkedin_draft.summary, linkedin_draft.profile_photo, linkedin_draft.recommendation, 
#             linkedin_draft.follow_company, linkedin_draft.join_group, linkedin_draft.public_url 
#             FROM linkedin_draft;
#             """
#         sql3 = """
#             SELECT linkedin_keyskill.id, linkedin_keyskill.draft_id, 
#             linkedin_keyskill.name FROM linkedin_keyskill;
#             """
#         sql4 = """
#             SELECT linkedin_education.id, linkedin_education.draft_id, linkedin_education.name, 
#             linkedin_education.level, linkedin_education.degree, linkedin_education.desc, 
#             linkedin_education.field, linkedin_education.study_from, linkedin_education.study_to, 
#             linkedin_education.current 
#             FROM linkedin_education
#             """
#         sql5 = """
#             SELECT linkedin_organization.id, linkedin_organization.draft_id, 
#             linkedin_organization.name, linkedin_organization.title, 
#             linkedin_organization.desc, linkedin_organization.work_from, 
#             linkedin_organization.work_to, linkedin_organization.current 
#             FROM linkedin_organization
#             """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
        
#         linkedin_df = pd.read_sql(sql2, con=db)
#         keyskill_df = pd.read_sql(sql3, con=db)
#         keyskill_df = keyskill_df.groupby(
#             'draft_id')['name'].apply(list).reset_index().rename(
#             columns={'name':'key_list', 'draft_id': 'id' })
#         linkedin_df = pd.merge(linkedin_df, keyskill_df, how='left',on='id')
#         del keyskill_df
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         education_df = pd.read_sql(sql4, con=db)
#         education_df = education_df.groupby(
#             'draft_id').apply(lambda x: x.to_dict(orient='records')).reset_index().rename(
#             columns={'draft_id': 'id', 0:'edu_list'})
#         linkedin_df = pd.merge(linkedin_df, education_df, how='left',on='id')
#         del education_df
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         organ_df = pd.read_sql(sql5, con=db)
#         organ_df = organ_df.groupby(
#             'draft_id').apply(lambda x: x.to_dict(orient='records')).reset_index().rename(
#             columns={'draft_id': 'id', 0:'org_list'})
#         linkedin_df = pd.merge(linkedin_df, organ_df, how='left',on='id')
#         del organ_df
        
#         update_values = []
#         update_sql = """
#                 INSERT INTO linkedin_draft 
#                 (created, modified, candidate_name, headline, summary, profile_photo,
#                 recommendation, follow_company, join_group, public_url, key_skills, cd_id) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                
#                 """
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Draft Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in linkedin_df.iterrows():
#             if row['id'] and row['id'] == row['id']:
#                 keyskills = ','.join(row['key_list']) if row['key_list'] and row['key_list'] == row['key_list'] else ''
#                 data_tup = (
#                     '2017-09-01 00:00:00',
#                     '2017-09-01 00:00:00',
#                     row['candidate_name'] if row['candidate_name'] and row['candidate_name'] == row['candidate_name'] else '',
#                     row['headline'] if row['headline'] and row['headline'] == row['headline'] else '',
#                     row['summary'] if row['summary'] and row['summary'] == row['summary'] else '',
#                     row['profile_photo'] if row['profile_photo'] and row['profile_photo'] == row['profile_photo'] else '',
#                     row['recommendation'] if row['recommendation'] and row['recommendation'] == row['recommendation'] else '',
#                     row['follow_company'] if row['follow_company'] and row['follow_company'] == row['follow_company'] else '',
#                     row['join_group'] if row['join_group'] and row['join_group'] == row['join_group'] else '',
#                     row['public_url'] if row['public_url'] and row['public_url'] == row['public_url'] else '',
#                     keyskills,
#                     row['id']
#                 )
#                 update_values.append(data_tup)    
#             if len(update_values) > 1000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
#                 cursor.executemany(update_sql, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql, update_values)
#             update_values = []
        
#         new_draft_df = pd.read_sql(
#             'SELECT linkedin_draft.id as new_id, linkedin_draft.cd_id as id FROM linkedin_draft ;',con=db2)
#         linkedin_df = pd.merge(linkedin_df, new_draft_df, how='left', on='id')
        
#         update_values = []
#         update_sql2 = """
#                 INSERT INTO linkedin_education 
#                 (created, modified, school_name, level, degree, edu_desc,
#                 field, study_from, study_to, edu_current, draft_id) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                
#                 """
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Education Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in linkedin_df.iterrows():
#             if row['edu_list'] and row['edu_list'] == row['edu_list']:
#                 edu_dict_list = row['edu_list']
#                 for edu in edu_dict_list:
#                     data_tup = (
#                         '2017-09-01 00:00:00',
#                         '2017-09-01 00:00:00',
#                         edu['name'] if edu['name'] and edu['name'] == edu['name'] else '',
#                         edu['level'] if edu['level'] and edu['level'] == edu['level'] else 1,
#                         edu['degree'] if edu['degree'] and edu['degree'] == edu['degree'] else '',
#                         edu['desc'] if edu['desc'] and edu['desc'] == edu['desc'] else '',
#                         edu['field'] if edu['field'] and edu['field'] == edu['field'] else '',
#                         edu['study_from'] if edu['study_from'] and edu['study_from'] == edu['study_from'] else None,
#                         edu['study_to'] if edu['study_to'] and edu['study_to'] == edu['study_to'] else None,
#                         edu['current'] if edu['current'] and edu['current'] == edu['current'] else 0,
#                         row['new_id']
#                     )
#                     update_values.append(data_tup)    
#             if len(update_values) > 1000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 cursor.executemany(update_sql2, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql2, update_values)
#             update_values = []
        
#         update_sql3 = """
#                 INSERT INTO linkedin_organization
#                 (created, modified, org_name, title, org_desc,
#                 work_from, work_to, org_current, draft_id) VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                
#                 """
        
        
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         print( 'Bulk Organization Insert Start')
#         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
#         for i, row in linkedin_df.iterrows():
#             if row['org_list'] and row['org_list'] == row['org_list']:
#                 org_dict_list = row['org_list']
#                 for org in  org_dict_list:
#                     data_tup = (
#                         '2017-09-01 00:00:00',
#                         '2017-09-01 00:00:00',
#                         org['name'] if org['name'] and org['name'] == org['name'] else '',
#                         org['title'] if org['title'] and org['title'] == org['title'] else 1,
#                         org['desc'] if org['desc'] and org['desc'] == org['desc'] else '',
#                         org['work_from'] if org['work_from'] and org['work_from'] == org['work_from'] else None,
#                         org['work_to'] if org['work_to'] and org['work_to'] == org['work_to'] else None,
#                         org['current'] if org['current'] and org['current'] == org['current'] else 0,
#                         row['new_id']
#                     )
#                     update_values.append(data_tup)    
#             if len(update_values) > 1000:
                
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Insert ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                
#                 cursor.executemany(update_sql3, update_values)
#                 update_values = []
                
#         if update_values:
#             cursor.executemany(update_sql3, update_values)
#             update_values = []
        
#         sql5 = """
#                 SELECT 
#                     cart_orderitem.id as oi_id, cart_orderitem.oio_linkedin_id as linked_id
#                 FROM cart_orderitem 
#                 INNER JOIN cart_order 
#                 ON ( cart_orderitem.order_id = cart_order.id ) 
#                 WHERE cart_order.added_on >= '2014-04-01 00:00:00' AND cart_orderitem.oio_linkedin_id IS NOT NULL
#                 ORDER BY cart_orderitem.added_on DESC
#                 """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         oi_df = pd.read_sql(sql5,con=db)
#         oi_df = pd.merge(oi_df, new_order_item_df, how='left', on='oi_id')
#         oi_df = oi_df[~oi_df.oi_new_id.isnull()]

#         del new_order_item_df
#         linkedin_df = linkedin_df[['id', 'new_id']]
#         linkedin_df = linkedin_df.rename(columns={'id': 'linked_id'})
#         oi_df = pd.merge(oi_df,  linkedin_df, how='left', on='linked_id')
        
#         coi_list = []
#         linked_id_list = []
#         for i, row in oi_df.iterrows():
#             coi_list.append(' WHEN {0} THEN {1} '.format(row['oi_new_id'], row['new_id']))
#             linked_id_list.append(str(row['oi_new_id']))
#             if len(linked_id_list) > 1000:
#                 update_sql = '''
#                     UPDATE order_orderitem SET oio_linkedin_id = (
#                     CASE id 
#                         {0}
#                     END) WHERE id IN ({1});
#                     '''.format(' '.join(coi_list), ', '.join(linked_id_list))

#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Update ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 db2.query(update_sql)
#                 update_sql = ''
#                 linked_id_list = []
#                 coi_list = []
#         if len(linked_id_list):
#             update_sql = '''
#                     UPDATE order_orderitem SET oio_linkedin_id = (
#                     CASE id 
#                         {0}
#                     END) WHERE id IN ({1});
#                     '''.format(' '.join(coi_list), ', '.join(linked_id_list))
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print( 'Bulk Update ' + str(i))
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             db2.query(update_sql)
#             update_sql = ''
#             linked_id_list = []
#             coi_list = []
#         del oi_df
#         print('Draft Order Items Migrated')
        
#         sql6 = """
#                 SELECT cart_orderitemoperation.id as oio_id, cart_orderitemoperation.linkedin_id as linked_id
#                 FROM cart_orderitemoperation 
#                 INNER JOIN cart_orderitem 
#                 ON ( cart_orderitemoperation.order_item_id = cart_orderitem.id ) 
#                 INNER JOIN cart_order 
#                 ON ( cart_orderitem.order_id = cart_order.id ) 
#                 WHERE cart_order.added_on >= '2014-04-01 00:00:00' AND cart_orderitemoperation.linkedin_id IS NOT NULL
#                 ORDER BY cart_orderitemoperation.added_on DESC;
#             """
#         db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
#         db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        
#         oio_df = pd.read_sql(sql6,con=db)
#         new_oio_df = pd.read_sql(
#             'SELECT order_orderitemoperation.id as new_oio_id, order_orderitemoperation.coio_id as oio_id FROM order_orderitemoperation;',con=db2)
#         oio_df = pd.merge(oio_df, new_oio_df, how='left', on='oio_id')
#         del new_oio_df
#         oio_df = oio_df[~oio_df.new_oio_id.isnull()]
#         oio_df = pd.merge(oio_df, linkedin_df, how='left', on='linked_id')
        

#         coio_list = []
#         linked_id_list = []
#         for i, row in oio_df.iterrows():
#             coio_list.append(' WHEN {0} THEN {1} '.format(row['new_oio_id'], row['new_id']))
#             linked_id_list.append(str(row['new_oio_id']))
#             if len(linked_id_list) > 1000:
#                 update_sql = '''
#                     UPDATE order_orderitemoperation SET linkedin_id = (
#                     CASE id 
#                         {0}
#                     END) WHERE id IN ({1});
#                     '''.format(' '.join(coio_list), ', '.join(linked_id_list))

#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 print( 'Bulk Update ' + str(i))
#                 print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 db2.query(update_sql)
#                 update_sql = ''
#                 linked_id_list = []
#                 coio_list = []
#         if len(linked_id_list):
#             update_sql = '''
#                 UPDATE order_orderitemoperation SET linkedin_id = (
#                 CASE id 
#                     {0}
#                 END) WHERE id IN ({1});
#                 '''.format(' '.join(coio_list), ', '.join(linked_id_list))

#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print( 'Bulk Update ' + str(i))
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             db2.query(update_sql)
#             update_sql = ''
#             linked_id_list = []
#             coio_list = []

#         print('Draft Order Item Operations Migrated')
#         del oio_df
#         