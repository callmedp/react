/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py resume_booster --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py products_review_update --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py jobs_from_shine_to_product --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py wallet_expire_daily --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py order_closer --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py linkedin_tips_email --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py feedback_call_entry --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py ltv_monthly_record --settings=careerplus.config.settings_live
#/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py cart_drop_out_mail --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py closeorders --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py update_product_buy_count --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py update_autocomplete --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py course_catalogue_cache_set --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py featured_profile --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py jobs_move_closing_update --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py close_neo_order_items --settings=careerplus.config.settings_live
/var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/manage.py service_expiry_reminder --settings=careerplus.config.settings_live

>>>>>>> origin/development
export DJANGO_SETTINGS_MODULE="careerplus.config.settings_live" && /var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/scripts/welcome_recording.py
export DJANGO_SETTINGS_MODULE="careerplus.config.settings_live" && /var/www/virtualenvs/learning/bin/python /var/www/site/learning/current/scripts/candidate_agent_interaction_recording.py