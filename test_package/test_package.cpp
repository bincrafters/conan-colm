#include <cstdlib>

#include "colm/colm.h"
#include "colm/program.h"

int main(int argc, const char* argv []) {
    colm_program* program = new colm_program;
    colm_set_debug(program, COLM_DBG_COMPILE);
    colm_delete_program(program);
    return EXIT_SUCCESS;
}
