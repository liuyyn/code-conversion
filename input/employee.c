/* employee.c */
#include <stdio.h>
#include <string.h>
#include <sqlca.h>
#include <sqlcpr.h>


/* Declare host variables */
int emp_id;
char emp_name[50];
float emp_salary;
char db_user[20];
char db_pass[20];

/* SQL Context and Cursor definitions */
void connect_db() {
    strcpy(db_user, "scott");
    strcpy(db_pass, "tiger");

    {
        struct sqlexd {
            unsigned short sqlvsn;
            unsigned short arrsiz;
            unsigned short iters;
            unsigned short offset;
            unsigned short selerr;
            unsigned short sqlety;
            unsigned short unused;
            const char *sqlstmt;
            void *sqldata;
            void *sqlind;
            struct sqlcxp *sqlctx;
            unsigned long sqlfpn;
        } sqlstm = {12, 1, 1, 0, 0, 1, 0, 
            "connect :db_user identified by :db_pass", 
            NULL, NULL, NULL, 0};

        sqlstm.sqldata = (void *)&db_user;
        sqlstm.sqlind = (void *)&db_pass;

        sqlcxt((void *)0, &sqlctx, &sqlstm, &sqlfpn);
    }
}

int fetch_employee(int id) {
    emp_id = id;

    {
        struct sqlexd {
            unsigned short sqlvsn;
            unsigned short arrsiz;
            unsigned short iters;
            unsigned short offset;
            unsigned short selerr;
            unsigned short sqlety;
            unsigned short unused;
            const char *sqlstmt;
            void *sqldata;
            void *sqlind;
            struct sqlcxp *sqlctx;
            unsigned long sqlfpn;
        } sqlstm = {12, 3, 1, 0, 0, 1, 0, 
            "select name, salary into :emp_name, :emp_salary from employees where id = :emp_id", 
            NULL, NULL, NULL, 0};

        void *sqldata[] = {emp_name, &emp_salary, &emp_id};
        void *sqlind[] = {NULL, NULL, NULL};

        sqlstm.sqldata = sqldata;
        sqlstm.sqlind = sqlind;

        sqlcxt((void *)0, &sqlctx, &sqlstm, &sqlfpn);
    }

    if (sqlca.sqlcode != 0) return 0;

    return 1;
}
