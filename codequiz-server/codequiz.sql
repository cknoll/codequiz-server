BEGIN TRANSACTION;
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
INSERT INTO "auth_permission" VALUES(1,'Can add permission',1,'add_permission');
INSERT INTO "auth_permission" VALUES(2,'Can change permission',1,'change_permission');
INSERT INTO "auth_permission" VALUES(3,'Can delete permission',1,'delete_permission');
INSERT INTO "auth_permission" VALUES(4,'Can add group',2,'add_group');
INSERT INTO "auth_permission" VALUES(5,'Can change group',2,'change_group');
INSERT INTO "auth_permission" VALUES(6,'Can delete group',2,'delete_group');
INSERT INTO "auth_permission" VALUES(7,'Can add user',3,'add_user');
INSERT INTO "auth_permission" VALUES(8,'Can change user',3,'change_user');
INSERT INTO "auth_permission" VALUES(9,'Can delete user',3,'delete_user');
INSERT INTO "auth_permission" VALUES(10,'Can add content type',4,'add_contenttype');
INSERT INTO "auth_permission" VALUES(11,'Can change content type',4,'change_contenttype');
INSERT INTO "auth_permission" VALUES(12,'Can delete content type',4,'delete_contenttype');
INSERT INTO "auth_permission" VALUES(13,'Can add session',5,'add_session');
INSERT INTO "auth_permission" VALUES(14,'Can change session',5,'change_session');
INSERT INTO "auth_permission" VALUES(15,'Can delete session',5,'delete_session');
INSERT INTO "auth_permission" VALUES(16,'Can add site',6,'add_site');
INSERT INTO "auth_permission" VALUES(17,'Can change site',6,'change_site');
INSERT INTO "auth_permission" VALUES(18,'Can delete site',6,'delete_site');
INSERT INTO "auth_permission" VALUES(19,'Can add poll',7,'add_poll');
INSERT INTO "auth_permission" VALUES(20,'Can change poll',7,'change_poll');
INSERT INTO "auth_permission" VALUES(21,'Can delete poll',7,'delete_poll');
INSERT INTO "auth_permission" VALUES(22,'Can add choice',8,'add_choice');
INSERT INTO "auth_permission" VALUES(23,'Can change choice',8,'change_choice');
INSERT INTO "auth_permission" VALUES(24,'Can delete choice',8,'delete_choice');
INSERT INTO "auth_permission" VALUES(25,'Can add log entry',9,'add_logentry');
INSERT INTO "auth_permission" VALUES(26,'Can change log entry',9,'change_logentry');
INSERT INTO "auth_permission" VALUES(27,'Can delete log entry',9,'delete_logentry');
INSERT INTO "auth_permission" VALUES(28,'Can add task',10,'add_task');
INSERT INTO "auth_permission" VALUES(29,'Can change task',10,'change_task');
INSERT INTO "auth_permission" VALUES(30,'Can delete task',10,'delete_task');
INSERT INTO "auth_permission" VALUES(31,'Can add task collection',11,'add_taskcollection');
INSERT INTO "auth_permission" VALUES(32,'Can change task collection',11,'change_taskcollection');
INSERT INTO "auth_permission" VALUES(33,'Can delete task collection',11,'delete_taskcollection');
INSERT INTO "auth_permission" VALUES(34,'Can add t c_ membership',12,'add_tc_membership');
INSERT INTO "auth_permission" VALUES(35,'Can change t c_ membership',12,'change_tc_membership');
INSERT INTO "auth_permission" VALUES(36,'Can delete t c_ membership',12,'delete_tc_membership');
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" datetime NOT NULL,
    "is_superuser" bool NOT NULL,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1,'pbkdf2_sha256$10000$fVV41GVjLxlN$NbDNeumoPZ+9qnVLpQvmMOTiOg/kO3GR8FL4H/ka0n8=','2013-07-08 11:32:24.124831',1,'ck','','','c.k.noll@gmx.de',1,1,'2013-06-07 18:00:06.908194');
INSERT INTO "auth_user" VALUES(2,'pbkdf2_sha256$10000$CTztfayF3asd$SqzAzOTT4CwzPsY+Uvf5dcXzMcFQJUDeapssMaY6kdE=','2013-07-13 09:37:29.962208',1,'Testadmin','','','',1,1,'2013-07-13 09:37:17.455976');
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
INSERT INTO "django_admin_log" VALUES(1,'2013-06-07 22:39:16.005370',1,8,'1','reprap',1,'');
INSERT INTO "django_admin_log" VALUES(2,'2013-06-07 22:44:48.795402',1,7,'1','What''s new?',2,'Added choice "django". Added choice "sms".');
INSERT INTO "django_admin_log" VALUES(3,'2013-06-07 22:51:20.048933',1,7,'2','Whats your Name?',1,'');
INSERT INTO "django_admin_log" VALUES(4,'2013-06-07 22:55:53.426505',1,7,'1','What''s new?',2,'Changed pub_date.');
INSERT INTO "django_admin_log" VALUES(5,'2013-06-08 00:27:15.854424',1,10,'1','TestTask11',1,'');
INSERT INTO "django_admin_log" VALUES(6,'2013-06-08 00:27:46.692208',1,10,'2','Test Task 22',1,'');
INSERT INTO "django_admin_log" VALUES(7,'2013-06-16 09:14:03.608502',1,10,'1','Funktions-Aufrufe1',2,'Changed title, pub_date and body_xml.');
INSERT INTO "django_admin_log" VALUES(8,'2013-06-16 09:15:04.190911',1,10,'2','Funktions-Aufrufe (Wdh.)2',2,'Changed title and body_xml.');
INSERT INTO "django_admin_log" VALUES(9,'2013-06-16 09:15:20.289464',1,10,'2','Funktions-Aufrufe (Wdh.)2',2,'Changed pub_date.');
INSERT INTO "django_admin_log" VALUES(10,'2013-06-16 09:15:38.240613',1,10,'2','Funktions-Aufrufe (Wdh.)2',2,'No fields changed.');
INSERT INTO "django_admin_log" VALUES(11,'2013-07-06 20:09:55.000632',1,3,'2','admin2',3,'');
INSERT INTO "django_admin_log" VALUES(12,'2013-07-06 20:12:03.686424',1,11,'1','TaskCollection object',1,'');
INSERT INTO "django_admin_log" VALUES(13,'2013-07-06 20:12:29.484970',1,11,'1','TaskCollection object',2,'Changed tasks.');
INSERT INTO "django_admin_log" VALUES(14,'2013-07-07 06:43:40.991829',1,11,'1','TaskCollection object',3,'');
INSERT INTO "django_admin_log" VALUES(15,'2013-07-07 09:37:33.129148',1,11,'1','TaskCollection object',1,'');
INSERT INTO "django_admin_log" VALUES(16,'2013-07-07 09:41:11.354387',1,11,'1','TC001:Test1',2,'Deleted t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(17,'2013-07-07 09:41:32.975056',1,11,'1','TC001:Test1',2,'Added t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(18,'2013-07-07 09:54:29.584287',1,11,'1','TC001:Test1',2,'Changed task for t c_ membership "TC_Membership object". Changed task and ordering for t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(19,'2013-07-07 09:54:47.107560',1,11,'1','TC001:Test1',2,'Changed ordering for t c_ membership "TC_Membership object". Changed ordering for t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(20,'2013-07-07 10:59:34.901676',1,11,'1','TC001:Test1',2,'Changed ordering for t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(21,'2013-07-07 11:03:24.113267',1,11,'1','TC001:Test1',2,'Changed ordering for t c_ membership "TC_Membership object".');
INSERT INTO "django_admin_log" VALUES(22,'2013-07-07 13:49:25.025391',1,10,'3','T003:Typumwandlung ',1,'');
INSERT INTO "django_admin_log" VALUES(23,'2013-07-07 13:59:21.255154',1,10,'3','T003:Typumwandlung ',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(24,'2013-07-07 14:00:06.511166',1,10,'3','T003:Typ-Umwandlung ',2,'Changed title and tag_list.');
INSERT INTO "django_admin_log" VALUES(25,'2013-07-07 14:08:20.573681',1,10,'3','T003:Typ-Umwandlung ',2,'Changed tag_list.');
INSERT INTO "django_admin_log" VALUES(26,'2013-07-07 14:13:46.045905',1,10,'4','T004:Syntax-Fehler',1,'');
INSERT INTO "django_admin_log" VALUES(27,'2013-07-07 14:26:41.657648',1,10,'4','T004:Syntax-Fehler',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(28,'2013-07-07 14:33:16.046898',1,10,'1','T001:Funktions-Aufrufe',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(29,'2013-07-07 14:36:21.568397',1,10,'4','T004:Syntax-Fehler',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(30,'2013-07-08 07:11:28.759571',1,10,'5','T005:Funktion mit beliebigen vielen Argumenten',1,'');
INSERT INTO "django_admin_log" VALUES(31,'2013-07-08 07:12:36.833314',1,10,'5','T005:Funktion mit beliebigen vielen Argumenten',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(32,'2013-07-08 07:56:37.220946',1,10,'6','T006:Indizierung 1',1,'');
INSERT INTO "django_admin_log" VALUES(33,'2013-07-08 08:02:16.866872',1,10,'7','T007:Indizierung 2',1,'');
INSERT INTO "django_admin_log" VALUES(34,'2013-07-08 08:02:31.621928',1,10,'6','T006:Indizierung 1',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(35,'2013-07-08 08:05:29.654694',1,11,'2','TC002:Python Grundlagen 1',1,'');
INSERT INTO "django_admin_log" VALUES(36,'2013-07-08 08:07:08.494880',1,10,'7','T007:Indizierung 2',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(37,'2013-07-08 11:39:43.861806',1,10,'4','T004:Syntax-Fehler',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(38,'2013-07-08 11:41:14.406496',1,10,'4','T004:Syntax-Fehler',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(39,'2013-07-08 11:43:48.562700',1,10,'5','T005:Funktion mit beliebigen vielen Argumenten',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(40,'2013-07-08 11:44:11.078384',1,10,'5','T005:Funktion mit beliebigen vielen Argumenten',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(41,'2013-07-08 11:46:00.380740',1,10,'5','T005:Funktion mit beliebigen vielen Argumenten',2,'No fields changed.');
INSERT INTO "django_admin_log" VALUES(42,'2013-07-08 11:47:50.026410',1,10,'6','T006:Indizierung 1',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(43,'2013-07-08 11:48:36.271150',1,10,'6','T006:Indizierung 1',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(44,'2013-07-08 11:48:53.957565',1,10,'6','T006:Indizierung 1',2,'No fields changed.');
INSERT INTO "django_admin_log" VALUES(45,'2013-07-08 11:49:41.557985',1,10,'7','T007:Indizierung 2',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(46,'2013-07-08 11:50:18.910756',1,10,'7','T007:Indizierung 2',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(47,'2013-07-08 11:50:53.622247',1,10,'7','T007:Indizierung 2',2,'Changed body_xml.');
INSERT INTO "django_admin_log" VALUES(48,'2013-07-08 11:51:03.349221',1,10,'6','T006:Indizierung 1',2,'No fields changed.');
INSERT INTO "django_admin_log" VALUES(49,'2013-07-08 21:51:53.608161',1,10,'8','T008:cbox_test',1,'');
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
INSERT INTO "django_content_type" VALUES(1,'permission','auth','permission');
INSERT INTO "django_content_type" VALUES(2,'group','auth','group');
INSERT INTO "django_content_type" VALUES(3,'user','auth','user');
INSERT INTO "django_content_type" VALUES(4,'content type','contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'session','sessions','session');
INSERT INTO "django_content_type" VALUES(6,'site','sites','site');
INSERT INTO "django_content_type" VALUES(7,'poll','polls_app','poll');
INSERT INTO "django_content_type" VALUES(8,'choice','polls_app','choice');
INSERT INTO "django_content_type" VALUES(9,'log entry','admin','logentry');
INSERT INTO "django_content_type" VALUES(10,'task','quiz','task');
INSERT INTO "django_content_type" VALUES(11,'task collection','quiz','taskcollection');
INSERT INTO "django_content_type" VALUES(12,'t c_ membership','quiz','tc_membership');
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
INSERT INTO "django_session" VALUES('lv5nn21ow8q9m4d5duao4qvoo6r3glk2','OTZmNzgxNTEwMDIyYjZiYWQ2MGMzOGJlYmIwMzljZGFiMGY0YzA3YzqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQRLAXUu','2013-07-20 20:11:23.016856');
INSERT INTO "django_session" VALUES('awerf8wxhqicoh38nc8lonl8ylejm0uw','OTZmNzgxNTEwMDIyYjZiYWQ2MGMzOGJlYmIwMzljZGFiMGY0YzA3YzqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQRLAXUu','2013-07-22 11:32:24.129086');
INSERT INTO "django_session" VALUES('xvji0t2ds6r9gn2xt60hhigs9615hwvh','OTljODVkYTM2ODA3MTkxZmI3NTY3ZmIwOTg4Y2U1NTVjMjg2M2RmNjqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQRLAnUu','2013-07-27 09:37:29.987337');
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
INSERT INTO "django_site" VALUES(1,'example.com','example.com');
CREATE TABLE "polls_app_choice" (
    "id" integer NOT NULL PRIMARY KEY,
    "poll_id" integer NOT NULL REFERENCES "polls_app_poll" ("id"),
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
INSERT INTO "polls_app_choice" VALUES(1,1,'reprap',0);
INSERT INTO "polls_app_choice" VALUES(2,1,'django',0);
INSERT INTO "polls_app_choice" VALUES(3,1,'sms',0);
INSERT INTO "polls_app_choice" VALUES(4,2,'Bert',0);
INSERT INTO "polls_app_choice" VALUES(5,2,'Bart',0);
INSERT INTO "polls_app_choice" VALUES(6,2,'Bastian',0);
CREATE TABLE "polls_app_poll" (
    "id" integer NOT NULL PRIMARY KEY,
    "question" varchar(200) NOT NULL,
    "pub_date" datetime NOT NULL
);
INSERT INTO "polls_app_poll" VALUES(1,'What''s new?','2012-06-07 18:21:04');
INSERT INTO "polls_app_poll" VALUES(2,'Whats your Name?','2013-06-07 22:51:18');
CREATE TABLE "quiz_task" (
    "id" integer NOT NULL PRIMARY KEY,
    "author" varchar(200) NOT NULL,
    "title" varchar(200) NOT NULL,
    "versionstring" varchar(20) NOT NULL,
    "pub_date" datetime NOT NULL,
    "body_xml" text NOT NULL,
    "tag_list" text NOT NULL
);
INSERT INTO "quiz_task" VALUES(1,'ck','Funktions-Aufrufe','1.0','2013-06-16 00:26:50','<?xml version="1.0"?>
<data>
    <txt>
        Gegeben sei der Quelltext:
    </txt>
    <src>
def func(a = 5, b = 7):
    print a, b        
    </src>
    <txt>
        Ergänzen Sie die von folgenden Funktionsaufrufen erzeugten Ausgaben
    </txt>
    <lelist>
        <elt>
            <src>func()</src><le len="10"/><sol>5 7</sol>
        </elt>
        <elt>
            <src>func(3)</src><le len="10"/><sol>3 7</sol>
        </elt>
        <elt>
            <src>func(3, ''test'')</src><le len="10"/><sol>3 test</sol>
        </elt>
    </lelist>
    <txt>
        <b>Hinweis:</b> siehe Kurs02 (Funktionen)
    </txt>
</data>','beta,basics');
INSERT INTO "quiz_task" VALUES(2,'ck','Funktions-Aufrufe (Wdh.)','1.0','2013-06-16 09:15:13','<?xml version="1.0"?>
<data>
    <txt>
        Gegeben sei der Quelltext:
    </txt>
    <src>
def func(a = 8, b = 7):
    print a, b        
    </src>
    <txt>
        Ergaenzen Sie die von folgenden Funktionsaufrufen erzeugten Ausgaben
    </txt>
    <lelist>
        <elt>
            <src>func()</src><le len="10"/><sol>8 7</sol>
        </elt>
        <elt>
            <src>func(3)</src><le len="10"/><sol>3 7</sol>
        </elt>
        <elt>
            <src>func(3, ''test'')</src><le len="10"/><sol>3 test</sol>
        </elt>
    </lelist>
    <txt>
        <b>Hinweis:</b> siehe Kurs02 (Funktionen)
    </txt>
</data>','beta,functions');
INSERT INTO "quiz_task" VALUES(3,'ck','Typ-Umwandlung ','1.0','2013-07-07 13:45:05','<?xml version="1.0"?>
<data>
    <txt>
        Vervollständigen Sie folgenden Quelltext mit zwei geeigneten Typumwandlungen, sodass die Ausgabe am Ende lautet: <TT>101</TT>
    </txt>
    <src>
a=10
b=1
    </src>
    <lelist>
        <elt>
            <le len="10"/><sol>a=str(a)</sol>
        </elt>
        <elt>
          <le len="10"/><sol>b=str(b)</sol>
        </elt>
    </lelist>
    <src>
print a + b # -> 101
    </src>
</data>','basics,beta');
INSERT INTO "quiz_task" VALUES(4,'ck','Syntax-Fehler','1.0','2013-07-07 14:12:16','<?xml version="1.0"?>
<data>
    <txt>
Die folgenden Code-Schnipsel enthalten zum Teil <i>Syntax</i>-Fehler. Korrigieren Sie ggf. den Quelltext (nur die fehlerhafte Zeile). Wenn kein Fehler vorliegen sollte, so lassen Sie das Eingabefeld leer.
    </txt>
<lelist>
        <elt>
    <src>
def schöneFunktion(a):
    return 2*a 
    </src>
<le len="10"/><sol>def schoeneFunktion(a):</sol>
    </elt>

        <elt>
    <src>
if a=b: print "gleich"
    </src>
<le len="10"/><sol>if a==b: print "gleich"</sol>
    </elt>

        <elt>
    <src>
a, b, c = b, c, a 
    </src>
<le len="10"/><sol></sol>
    </elt>
    </lelist>
</data>','beta,basics');
INSERT INTO "quiz_task" VALUES(5,'ck','Funktion mit beliebigen vielen Argumenten','1.0','2013-07-08 07:09:07','<?xml version="1.0"?>
<data>
    <txt>
Schreiben Sie eine Funktion namens func1, die beliebig viele (unbenannte) Argumente empfangen kann nichts tut und nichts zurückgibt.
<br><br>
<b>Hinweise:</b> Die Muster-Lösung hat zwei Zeilen und verwendet vier Leerzeichen pro Einrückungsebene.
    </txt>
    <lelist>
        <elt>
            <le len="10"/><sol>def func1(*args):</sol>
        </elt>
        <elt>
            <le len="10"/><sol>    pass</sol>
        </elt>
    </lelist>
</data>','beta, basics');
INSERT INTO "quiz_task" VALUES(6,'ck','Indizierung 1','1.0','2013-07-08 07:56:34','<?xml version="1.0"?>
<data>
    <txt>
        Ergänzen sie jeweils das Ergebnis folgender Code-Zeilen (ohne Leerzeichen).
<br><br>
<b>Hinweise:</b> Beispiel-Liste: <tt>[8,9,10]</tt>, Beispiel-String: <tt>"Hallo Welt"</tt>
    </txt>
    <lelist>
        <elt>
            <src>range(3)</src><le len="10"/><sol>[0,1,2]</sol>
        </elt>
        <elt>
            <src>"Hallo Welt"[1]</src><le len="10"/><sol>"a"</sol>
        </elt>
        <elt>
            <src>"Hallo Welt"[:4]</src><le len="10"/><sol>"Hall"</sol>
        </elt>
        <elt>
            <src>"Hallo Welt"[-3]</src><le len="10"/><sol>"e"</sol>
        </elt>
        <elt>
            <src>"Hallo Welt"[-3:]</src><le len="10"/><sol>"elt"</sol>
        </elt>
        <elt>
            <src>"Hallo Welt"[1:5]</src><le len="10"/><sol>"allo"</sol>
        </elt>
    </lelist>
</data>','beta, basics');
INSERT INTO "quiz_task" VALUES(7,'ck','Indizierung 2','1.0','2013-07-08 07:57:24','<?xml version="1.0"?>
<data>
    <txt>
        Ergänzen sie jeweils das Ergebnis folgender Code-Zeilen (ohne Leerzeichen).
<br><br>
<b>Hinweise:</b> Beispiel-Liste: <tt>[8,9,10]</tt>, Beispiel-String: <tt>"Hallo Welt"</tt>, Beispiel-Bool: <tt>False</tt>
    </txt>
    <lelist>
        <elt>
            <src>[1,5]*3</src><le len="10"/><sol>[1,5,1,5,1,5]</sol>
        </elt>
        <elt>
            <src>"-"*3</src><le len="10"/><sol>"---"</sol>
        </elt>
        <elt>
            <src>"abc" == ''abc''</src><le len="10"/><sol>True</sol>
        </elt>
        <elt>
            <src>8 in range(10)</src><le len="10"/><sol>True</sol>
        </elt>
        <elt>
            <src>"all" in ''Hallo''</src><le len="10"/><sol>True</sol>
        </elt>
        <elt>
            <src>"g" not in "[a-z]" </src><le len="10"/><sol>True</sol>
        </elt>
    </lelist>
</data>','beta, basics');
INSERT INTO "quiz_task" VALUES(8,'ck','cbox_test','1.0','2013-07-08 21:40:32','<?xml version="1.0"?>
<data>
    <txt>
        Richtig oder Falsch?
<br><br>
<b>Hinweise:</b> Denken Sie nach!
    </txt>
    <input_list>
        <elt>
            <src>[1,5]*3</src><le len="10"/><sol>[1,5,1,5,1,5]</sol>
        </elt>
        <elt>
            <src>[1,5]***3</src><cbox label=''Richtig?''/><sol>False</sol>
        </elt>
    </input_list>
</data>','test');
CREATE TABLE "quiz_taskcollection" (
    "id" integer NOT NULL PRIMARY KEY,
    "author" varchar(200) NOT NULL,
    "title" varchar(200) NOT NULL
);
INSERT INTO "quiz_taskcollection" VALUES(1,'ck','Test1');
INSERT INTO "quiz_taskcollection" VALUES(2,'ck','Python Grundlagen 1');
CREATE TABLE "quiz_taskcollection_tasks" (
    "id" integer NOT NULL PRIMARY KEY,
    "taskcollection_id" integer NOT NULL,
    "task_id" integer NOT NULL REFERENCES "quiz_task" ("id"),
    UNIQUE ("taskcollection_id", "task_id")
);
INSERT INTO "quiz_taskcollection_tasks" VALUES(1,1,1);
INSERT INTO "quiz_taskcollection_tasks" VALUES(2,1,2);
CREATE TABLE "quiz_tc_membership" (
    "id" integer NOT NULL PRIMARY KEY,
    "task_id" integer NOT NULL REFERENCES "quiz_task" ("id"),
    "group_id" integer NOT NULL REFERENCES "quiz_taskcollection" ("id"),
    "ordering" real NOT NULL
);
INSERT INTO "quiz_tc_membership" VALUES(2,1,1,10.0);
INSERT INTO "quiz_tc_membership" VALUES(3,2,1,12.0);
INSERT INTO "quiz_tc_membership" VALUES(4,4,2,10.0);
INSERT INTO "quiz_tc_membership" VALUES(5,1,2,20.0);
INSERT INTO "quiz_tc_membership" VALUES(6,3,2,30.0);
INSERT INTO "quiz_tc_membership" VALUES(7,5,2,40.0);
INSERT INTO "quiz_tc_membership" VALUES(8,6,2,50.0);
INSERT INTO "quiz_tc_membership" VALUES(9,7,2,60.0);
CREATE INDEX "auth_permission_37ef4eb4" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_5f412f9a" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_83d7f98b" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_6340c63c" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_5f412f9a" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_user_user_permissions_6340c63c" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_83d7f98b" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "django_session_b7b81f0c" ON "django_session" ("expire_date");
CREATE INDEX "polls_app_choice_70f78e6b" ON "polls_app_choice" ("poll_id");
CREATE INDEX "django_admin_log_6340c63c" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_37ef4eb4" ON "django_admin_log" ("content_type_id");
CREATE INDEX "quiz_taskcollection_tasks_1060e6c1" ON "quiz_taskcollection_tasks" ("taskcollection_id");
CREATE INDEX "quiz_taskcollection_tasks_ef96c3b8" ON "quiz_taskcollection_tasks" ("task_id");
CREATE INDEX "quiz_tc_membership_ef96c3b8" ON "quiz_tc_membership" ("task_id");
CREATE INDEX "quiz_tc_membership_5f412f9a" ON "quiz_tc_membership" ("group_id");
COMMIT;
