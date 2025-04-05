/* logic.c */
#include <stdio.h>

extern int emp_id;
extern char emp_name[50];
extern float emp_salary;

extern int fetch_employee(int id);

float increase_salary(float salary, float percent) {
    return salary + (salary * percent / 100.0);
}

void process_employee(int id) {
    if (fetch_employee(id)) {
        float new_salary = increase_salary(emp_salary, 10.0);
        printf("Updated salary for %s (ID %d): %.2f\n", emp_name, emp_id, new_salary);
    } else {
        printf("Employee ID %d not found.\n", id);
    }
}
