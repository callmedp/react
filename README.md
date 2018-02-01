# careerplus

# Os Setup

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev libmysqlclient-dev
sudo apt-get install libcairo2-dev
sudo apt-get install python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0.0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

sudo pip3 install virtualenv virtualenvwrapper
cp ~/.bashrc ~/.bashrc-org
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc

# Env Setup

mkvirtualenv careerplus
pip install geoip
pip3 install -r requirements/common.txt
sudo apt-get install mysql-server
mkdir /etc/uwsgi/
mkdir /etc/uwsgi/apps-available/
create uwsgi files
mkdir /etc/uwsgi/vassals
sudo ln -s /etc/uwsgi/apps-available/careerplus.ini /etc/uwsgi/vassals/
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

# Data Setup
#python manage.py makemigrations
#python manage,py makemigrations thumbnails
python manage.py migrate


SQL collate error fix:
ALTER DATABASE careerplus CHARACTER SET utf8 COLLATE utf8_general_ci;

SELECT CONCAT('ALTER TABLE ', a.table_name, ' CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;') FROM information_schema.tables a WHERE a.table_schema = 'careerplus';

Copy queries and run

# Fixtures
# python manage.py cities_light
python manage.py loaddata pdata.json
python manage.py loaddata shop.json
python manage.py loaddata blog.json
python manage.py loaddata mdata.json
python manage.py loaddata geolocation.json
python manage.py loaddata shopdata.json

make entry in hosts files
172.22.67.111 sumosc.shine.com sumosc1.shine.com
172.22.65.64 recruiter.shine.com
172.22.65.140 www.shine.com

Add access to Mysql
https://stackoverflow.com/questions/19101243/error-1130-hy000-host-is-not-allowed-to-connect-to-this-mysql-server


# Install redis
apt-get install redis-server
https://www.rosehosting.com/blog/how-to-install-configure-and-use-redis-on-ubuntu-16-04/

# Setup crons
apt-get install cron
cd /opt/
mkdir crons
cd crons
mkdir logs
# create cron scripts daily/weekly/etc
crontab -e

#start a screen for celery
cd /code/careerplus
workon careerplus
celery multi restart w1 -A careerplus -l debug --logfile=/var/log/celery/w1.log --pidfile=/var/log/celery/w1.pid
#upload skills and FA
scp '/path-to/Courses-FA.csv' vijay1@172.22.65.33:/tmp/
scp '/path-to/Courses-Skill.csv' vijay1@172.22.65.33:/tmp/

#in shell
upload_Skill('/tmp/Courses-Skill.csv')
upload_FA('/tmp/Courses-FA.csv')

CREATE USER 'root'@'10.24.8.130';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.24.8.130' IDENTIFIED BY 'root';



(
select
    details.order_id as Order_Id,
    details.email,
    details.Sales_executive,
    details.Sales_TL,
    details.Branch_Head,
    details.sales_user_info,
    details.Owner_name,
    details.Order_Date,
    details.Payment_Date,
    details.item_id as Item_Id,
    details.Type_flow as Type_flow,
    details.Item_Level as Item_Level,
    details.Item_Name as Item_Name,

    discinfo.GrossPrice_Order as GrossPrice_Order,
    discinfo.NetPrice_Order as NetPrice_Order,
    discinfo.NetDiscount as EffectiveDiscount_Order,

    details.Item_Price as NetPrice_Item,

    (((100-discinfo.NetDiscount)/100)*details.Item_Price) as EffectivePrice_Item,

    discinfo.CouponCode as Coupon_Code,
    discinfo.CouponDiscount as Coupon_Discount,
    discinfo.status as status,

    details.Transaction_ID,
    details.Transaction_Amount,
    details.Payment_mode

    from
        (
        select
            coi.order_id,
            replace(replace(replace(replace(substring_index(SUBSTRING_INDEX(co.sales_user_info, 'executive', -1),',',1),",",''),"'",""),"}",""),":","") as Sales_executive,
            replace(replace(replace(replace(SUBSTRING_INDEX(SUBSTRING_INDEX(co.sales_user_info, 'team_lead', -1),',',1),",",''),"'",""),"}",""),":","") as Sales_TL,
            replace(replace(replace(replace(SUBSTRING_INDEX(SUBSTRING_INDEX(co.sales_user_info, 'branch_head', -1),',',1),",",''),"'",""),"}",""),":","") as Branch_Head,
            sales_user_info,
            date(co.created) as Order_Date,
            date(co.payment_date) as Payment_Date,
            co.email as Email,
            coi.selling_price as Item_Price,
            coi.id as item_id,
            c_sp.type_flow as Type_flow,
            cp.name as Item_Level,
            pv.name as Owner_name,
            c_pp.Payment_mode,
            c_pp.Transaction_ID,
            c_pp.Transaction_Amount,
            IFNULL(cp_coi.name,cp.name) as Item_Name

            from

            careerplus.order_orderitem as coi

            left join

            careerplus.order_order as co
            on coi.order_id=co.id

            left join

            careerplus.shop_product as c_sp
            on c_sp.id=coi.product_id

            left join

            (
            select
                order_id,
                GROUP_CONCAT(txn ORDER BY txn ASC SEPARATOR ', ') as Transaction_ID,
                GROUP_CONCAT(
                    CASE
                    WHEN Payment_mode = '0' THEN 'Not Paid'
                    WHEN Payment_mode = '1' THEN 'Cash/Payment.Shine.com'
                    WHEN Payment_mode = '2' THEN 'Citrus_Pay'
                    WHEN Payment_mode = '3' THEN 'EMI'
                    WHEN Payment_mode = '4' THEN 'Cheque or Draft'
                    WHEN Payment_mode = '5' THEN 'CC-Avenue'
                    WHEN Payment_mode = '6' THEN 'Mobikwik'
                    WHEN Payment_mode = '7' THEN 'CC-Avenue-International'
                    WHEN Payment_mode = '8' THEN 'Debit Card'
                    WHEN Payment_mode = '9' THEN 'Credit Card'
                    WHEN Payment_mode = '10' THEN 'Net Banking'
                    END
                    ORDER BY txn ASC SEPARATOR ', ') as Payment_mode,
                GROUP_CONCAT(txn_amount ORDER BY txn ASC SEPARATOR ', ') as Transaction_Amount
                from
                careerplus.payment_paymenttxn
                group by order_id
            ) as c_pp
            on c_pp.order_id=co.id

            left join

            careerplus.shop_product as cp
            on coi.product_id=cp.id

            left join

            partner_vendor as pv
            on pv.id=cp.vendor_id

            left join

            (
            select
                coi_2.id,cp2.name from careerplus.order_orderitem as coi_2
                left join careerplus.order_orderitem as coi_3
                on coi_2.parent_id=coi_3.id
                left join careerplus.shop_product as cp2
                on cp2.id=coi_3.product_id
            ) as cp_coi
            on cp_coi.id=coi.id

            where date(co.payment_date) >= date_add(curdate(), interval -1 day)
            and co.status not in (0)
            order by 1 desc
        ) as details
        left join
        (
        select
            oi.order_id,
            oi.Items_Count as items,
            ed.GrossPrice_Order,
            ed.NetPrice_Order,
            ed.NetDiscount,
            oi.status,
            IFNULL(ed.coupon_id,'No Discount Coupon Offered') as CouponCode,
            IFNULL(ed.Coupon_Discount,'0') as CouponDiscount,
            if(ed.NetDiscount=0,'0',round((1-pow(((100-ed.NetDiscount)/100),1/(oi.Items_Count)))*100,0))as DistributedDiscount
            from
            (
                 #Calculating the number of items in each order
                 select coi.order_id,co.status,
                         count(*) as Items_Count
                 from careerplus.order_orderitem as coi
                 left join careerplus.order_order as co
                 on coi.order_id=co.id

                 where co.status not in (0)

                 group by 1
                 order by 1 desc
            ) as oi
            left join
            (
            #Getting effective discount for each order
            select
                co.id as order_id,
                op.GrossPrice_Order,
                co.TOTAL_INCL_TAX as NetPrice_Order,
                if(op.GrossPrice_Order-co.TOTAL_INCL_TAX=0,'NoDiscountOffered',round(((op.GrossPrice_Order-co.TOTAL_INCL_TAX)/op.GrossPrice_Order)*100,0))as NetDiscount,
                c_oc.coupon_id,
                cc.value as Coupon_Discount
                from careerplus.order_order as co
                left join (select order_id,sum(selling_price) as GrossPrice_Order from careerplus.order_orderitem group by 1) as op
                on co.id=op.order_id
                left join careerplus.order_couponorder as c_oc
                on c_oc.order_id = co.id
                left join careerplus.coupon_coupon as cc
                on c_oc.coupon_code=cc.code
                order by 1 desc
            ) as ed
             on oi.order_id=ed.order_id
             order by 1 desc
        ) as discinfo
    on details.order_id=discinfo.order_id
) as A



















for oi in OrderItem.objects.filter(order__payment_date__gte=datetime.datetime(2018,1,1),order__status__in=[1,2,3,4]):
    a = reduce(lambda x,y: x + y,[x.selling_price for x in oi.order.orderitems.all()])
    b = oi.order.total_incl_tax
    c = re.sub("'","\"",oi.order.sales_user_info)
    if c:
        c = json.loads(c)
    if a:
        d = round((a - b)*100/a, 2)
    print(
    oi.order.id,
    oi.order.email,
    oi.partner.name if oi.partner else '',
    oi.order.created,
    oi.order.payment_date,
    oi.order.crm_sales_id,
    c['team_lead'] if c else '',
    c['branch_head'] if c else '',
    ', '.join([tx.txn for tx in oi.order.get_txns()]),
    oi.id,
    oi.product.get_type_flow_display(),
    oi.product.name,
    oi.order.get_status_display(),
    a,
    b,
    d,
    oi.selling_price,
    (100-d)*oi.selling_price/100,
    ', '.join([str(tx.txn_amount) for tx in oi.order.get_txns()]),
    ', '.join([str(o.coupon_code) for o in oi.order.couponorder_set.all()]),
    ', '.join([tx.get_payment_mode_display() for tx in oi.order.get_txns()]),
    ', '.join([str(o.value) for o in oi.order.couponorder_set.all()]),
    sep=";"
    )
    
    
csvfile = open('/tmp/report_9.csv','w')
writer=csv.writer(csvfile, delimiter=';')
for oi in OrderItem.objects.filter(order__payment_date__gte=timezone.datetime(2018,1,1),
order__payment_date__lte=datetime.datetime(2018,1,31),order__status__in=[1,2,3,4]):
    a = reduce(lambda x,y: x + y,[x.selling_price for x in oi.order.orderitems.filter(no_process=False)])
    b = oi.order.total_incl_tax
    c = re.sub("'","\"",oi.order.sales_user_info)
    if c:
        c = json.loads(c)
    d = round((a - b)*100/a, 2) if a else 0
    e = [
    oi.order.id,
    oi.order.email,
    oi.partner.name if oi.partner else '',
    oi.order.created,
    oi.order.payment_date,
    oi.order.crm_sales_id,
    c['team_lead'] if c else '',
    c['branch_head'] if c else '',
    ', '.join([tx.txn for tx in oi.order.get_txns()]),
    oi.id,
    oi.product.get_type_flow_display(),
    oi.product.name,
    oi.order.get_status_display(),
    a,
    b,
    d,
    oi.selling_price,
    (100-d)*oi.selling_price/100,
    ', '.join([str(tx.txn_amount) for tx in oi.order.get_txns()]),
    ', '.join([str(o.coupon_code) for o in oi.order.couponorder_set.all()]),
    ', '.join([tx.get_payment_mode_display() for tx in oi.order.get_txns()]),
    ', '.join([str(o.value) for o in oi.order.couponorder_set.all()])    
    ]
    writer.writerow(e)














