all:
ifndef TARGET_FILENAME
	$(error TARGET_FILENAME not defined)
endif

	i686-w64-mingw32-windres src/resource.rc -O coff -o resource.o

	i686-w64-mingw32-objcopy --input-target binary --output-target elf32-i386 --binary-architecture i386 \
	src/bootstrap.ps1 bootstrap.o \
	--redefine-sym "_binary_src_bootstrap_ps1_start"="_binary_bootstrap_start" \
	--redefine-sym "_binary_src_bootstrap_ps1_end"="_binary_bootstrap_end"

	i686-w64-mingw32-objcopy --input-target binary --output-target elf32-i386 --binary-architecture i386 \
	config.json config.o \
	--redefine-sym "_binary_config_json_start"="_binary_config_start" \
	--redefine-sym "_binary_config_json_end"="_binary_config_end"

	i686-w64-mingw32-objcopy --input-target binary --output-target elf32-i386 --binary-architecture i386 \
	src/setup.py setup.o \
	--redefine-sym "_binary_src_setup_py_start"="_binary_setup_start" \
	--redefine-sym "_binary_src_setup_py_end"="_binary_setup_end"

	i686-w64-mingw32-gcc -o binary.exe -O3 -Wall \
	src/main.c resource.o config.o bootstrap.o setup.o

	mv binary.exe $(TARGET_FILENAME)

	rm resource.o
	rm config.o
	rm bootstrap.o
	rm setup.o
