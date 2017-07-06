import MySQLdb

def get_user(user_id) :
    sql_user = 'root'
    database = 'edxapp'
    sql_passwd = ""


    try:
        db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
    except:
        print "MySQL connection not established"

    query = "select username from auth_user where id= %s"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query, (user_id,))
    user_name = mysql_cursor.fetchall()
    return user_name[0][0]

def is_present(username, course_name, db_mysql) :
    query = "select count(username) from suspicious_count where username=%s and course_name=%s"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query, (username, course_name))
    boolean_val = mysql_cursor.fetchall()
    return boolean_val[0][0]
    

def update_table(user_id, course_name, column_name, value) :
    sql_user = 'root'
    database = 'edxapp'
    sql_passwd = ""

    username = get_user(user_id)

    try:
        db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
    except:
        print "MySQL connection not established"

    present_bool = is_present(username, course_name, db_mysql)

    if present_bool :
	if column_name == "img_count" :
        	update_query = "update suspicious_count set img_count = %s where username=%s and course_name=%s"
		get_query = "select img_count from suspicious_count where username=%s and course_name=%s"
	else :
		update_query = "update suspicious_count set web_count = %s where username=%s and course_name=%s"
                get_query = "select web_count from suspicious_count where username=%s and course_name=%s"


        mysql_cursor = db_mysql.cursor()
	mysql_cursor.execute(get_query, (username, course_name))
        original_value = mysql_cursor.fetchall()
	mysql_cursor.execute(update_query, (value + original_value[0][0], username, course_name))

	db_mysql.commit()

    else :
	insert_query = "insert into suspicious_count (username, course_name, web_count, img_count, tot_count) values (%s, %s, %s, %s, %s)"
	mysql_cursor = db_mysql.cursor()

        if column_name == "web_count" : 
            mysql_cursor.execute(insert_query, (username, course_name, value, 0, value))
        else :
            mysql_cursor.execute(insert_query, (username, course_name, 0, value, value))

	db_mysql.commit()
            


        
def final_result(course_name) :
    sql_user = 'root'
    database = 'edxapp'
    sql_passwd = ""


    try:
        db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
    except:
        print "MySQL connection not established"

    query = "select username from suspicious_count where course_name=%s order by tot_count desc"
    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query, (course_name,))
    ordered_user = mysql_cursor.fetchall()
    
    suspicious_rank = []    

    for student in ordered_user:
	suspicious_rank.append(student[0])

    return suspicious_rank
	

def update_total() :
	sql_user = 'root'
   	database = 'edxapp'
    	sql_passwd = ""


    	try:
            db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
    	except:
            print "MySQL connection not established"	

	query = "update suspicious_count set tot_count = img_count + web_count"
	mysql_cursor = db_mysql.cursor()
    	mysql_cursor.execute(query, ())

	db_mysql.commit()

def reset_table() :
	sql_user = 'root'
        database = 'edxapp'
        sql_passwd = ""


        try:
            db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
        except:
            print "MySQL connection not established"
	
        query_web = "update suspicious_count set web_count = 0"
	query_img = "update suspicious_count set img_count = 0"
	query_tot = "update suspicious_count set tot_count = 0"
	query_com = "update suspicious_count set img_match = 'NULL'"

	mysql_cursor = db_mysql.cursor()
	mysql_cursor.execute(query_web, ())
	mysql_cursor.execute(query_img, ())
	mysql_cursor.execute(query_tot, ())
	mysql_cursor.execute(query_com, ())

	db_mysql.commit()

