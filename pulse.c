// pulse.c  - reads computers vital signs and prints as JSON
#include <stdio.h>

#define TEMP_MISSING -999.0

double uptime(void);
long memory(void);
double cpuTemp(void);

int main(void) {
    double up_seconds = uptime();
    
    long mem_kb = memory();

    double cpu_temp = cpuTemp();

    if (cpu_temp == 0){
        printf("{\"uptime_s\": %.0f, \"mem_available_kb\": %ld, \"cpu_temp_c\": null}\n", up_seconds, mem_kb);
    } 
    else {
        printf("{\"uptime_s\": %.0f, \"mem_available_kb\": %ld, \"cpu_temp_c\": %0f}\n", up_seconds, mem_kb, cpu_temp);
    }
    return 0;
}

double uptime(void){
    FILE *f = fopen("/proc/uptime", "r");
    if (f == NULL) {
        fprintf(stderr, "could not open /proc/uptime\n");
        return -1;
    }

    double up_seconds;
    if (fscanf(f, "%lf", &up_seconds) != 1) {
        fclose(f);
        return -1;
    }
    fclose(f);
    return up_seconds;
}

long memory(void){
    FILE *f = fopen("/proc/meminfo", "r");
    if (f == NULL) {
        fprintf(stderr, "could not open /proc/meminfo\n");
        return -1;
    }

    char line[256];
    long mem_kb;
    while (fgets(line, sizeof(line), f) != NULL) {
        if (sscanf(line, "MemAvailable: %ld kB", &mem_kb) == 1){
            fclose(f);
            return mem_kb;
        }
    }

    fclose(f);
    fprintf(stderr, "MemAvailable not found\n");
    return -1;
}



double cpuTemp(void){
    FILE *f = fopen ("/sys/class/thermal/thermal_zone0/temp", "r");
    if (f == NULL){
        return 0;
    }

    double cpu_temp;
    if (fscanf(f, "%lf", &cpu_temp) != 1){
        fclose(f);
        return -1;
    }
    fclose(f);
    cpu_temp = cpu_temp / 1000.0;
    return cpu_temp;
}