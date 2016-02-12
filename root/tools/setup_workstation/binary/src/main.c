#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>


void write_error(char *error) {
    fprintf(stderr, error);
}


/* Set as an exit handler by atexit - Pauses before closing so that the logging is viewable */
void exit_prompt(void) {
    printf("Press any key to close\n");
    getchar();
}


/*  Set as an exit handler by atexit - Remove temporary files */
void cleanup_environment(void) {
    printf("Cleaning up...\n");

    /* We don't care if these fail, so don't check return values */
    remove("C:\\Cilix\\config.json");
    remove("C:\\Cilix\\bootstrap.ps1");
    remove("C:\\Cilix\\setup.py");
}


/*  Dump the config binary object to a file */
int write_config_file(void) {
    extern char binary_config_start, binary_config_end;
    FILE *descriptor;

    printf("  Writing config file...\n");

    descriptor = fopen("C:\\Cilix\\config.json", "w");
    if(descriptor == NULL) {
        write_error("    Failed to open config.json\n");
        return -1;
    }

    if(fwrite(&binary_config_start, (&binary_config_end - &binary_config_start), 1, descriptor) == -1) {
        write_error("    Failed to write config.json\n");
        return -1;
    }

    if(fclose(descriptor) == EOF) {
        write_error("    Failed to close config.json\n");
        return -1;
    }

    return 0;
}


/*  Dump the bootstrap binary object to a file */
int write_bootstrap(void) {
    extern char binary_bootstrap_start, binary_bootstrap_end;
    FILE *descriptor;

    printf("  Writing bootstrap script...\n");

    descriptor = fopen("C:\\Cilix\\bootstrap.ps1", "w");
    if(descriptor == NULL) {
        write_error("    Failed to open bootstrap.ps1\n");
        return -1;
    }

    if(fwrite(&binary_bootstrap_start, (&binary_bootstrap_end - &binary_bootstrap_start), 1, descriptor) == -1) {
        write_error("    Failed to write bootstrap.ps1\n");
        return -1;
    }

    if(fclose(descriptor) == EOF) {
        write_error("    Failed to close bootstrap.ps1\n");
        return -1;
    }

    return 0;
}


/*  Dump the setup binary object to a file */
int write_setup(void) {
    extern char binary_setup_start, binary_setup_end;
    FILE *descriptor;

    printf("  Writing setup script...\n");

    descriptor = fopen("C:\\Cilix\\setup.py", "w");
    if(descriptor == NULL) {
        write_error("    Failed to open setup.py\n");
        return -1;
    }

    if(fwrite(&binary_setup_start, (&binary_setup_end - &binary_setup_start), 1, descriptor) == -1) {
        write_error("    Failed to write setup.py\n");
        return -1;
    }

    if(fclose(descriptor) == EOF) {
        write_error("    Failed to close setup.py\n");
        return -1;
    }

    return 0;
}


/*  Create the root folder structure */
int prepare_environment(void) {
    printf("Preparing environment...\n");
    printf("  Creating root directory...\n");

    if(chdir("C:\\") == -1) {
        write_error("    Failed to change working directory\n");
    }

    /* Note that since we're compiling with MinGW this doesn't follow the UNIX standard arguments */
    if(mkdir("C:\\Cilix") == -1) {
        if(errno != EEXIST) {
            write_error("    Failed to create root directory\n");
            return -1;
        }
    }

    if(write_config_file() == -1) {
        return -1;
    }

    if(write_bootstrap() == -1) {
        return -1;
    }

    if(write_setup() == -1) {
        return -1;
    }

    return 0;
}


/* Run the bootstrap script */
int run_bootstrap(void) {
    printf("Running bootstrap...\n");

    if(system("powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted") != 0) {
        write_error("  Failed to set execution policy\n");
        return -1;
    }

    if(system("powershell -File C:\\Cilix\\bootstrap.ps1") != 0) {
        write_error("  Failed to start bootstrap\n");
        return -1;
    }

    return 0;
}


int run_setup(void) {
    printf("Running setup...\n");

    if(system("C:\\Cilix\\Python\\python.exe C:\\Cilix\\setup.py") != 0) {
        write_error("  Failed to start setup\n");
        return -1;
    }

    return 0;
}


int main(int argc, char *argv[]) {
    if(atexit(exit_prompt) != 0) {
        write_error("Failed to set exit_prompt exit handler\n");
        return EXIT_FAILURE;
    }

    if(atexit(cleanup_environment) != 0) {
        write_error("Failed to set cleanup_environment exit handler\n");
        return EXIT_FAILURE;
    }

    if(prepare_environment() == -1) {
        return EXIT_FAILURE;
    }

    if(run_bootstrap() == -1) {
        return EXIT_FAILURE;
    }

    if(run_setup() == -1) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
