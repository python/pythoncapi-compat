// C extension made of two C files (extension.c and static_inline.c) to detect
// when a pythoncapi_compat.h function is implemented without "static inline".

#include "pythoncapi_compat.h"

// No function defined, only #include "pythoncapi_compat.h"
