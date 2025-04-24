/* main.c - Precompiled version of main.pc */
#include <stdio.h>
#include <sqlca.h>
#include <sqlcpr.h>  // Required for OCI runtime

#include <empstructs.h> 
/* External C functions from other modules */
// void connect_db();
// void process_employee(int id);

/* SQL Context */
void *sqlctx;
unsigned long sqlfpn;

int main() {
    /* Connect to DB using generated function */
    connect_db();

    /* Process employees */
    process_employee(101);
    process_employee(202);
    process_employee(999);

    /* Precompiled form of: EXEC SQL COMMIT WORK RELEASE */
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
        } sqlstm = {12, 0, 1, 0, 0, 0, 0, 
            "commit work release", 
            NULL, NULL, NULL, 0};

        sqlcxt((void *)0, &sqlctx, &sqlstm, &sqlfpn);
    }

    printf("Disconnected from DB.\n");
    return 0;
}
