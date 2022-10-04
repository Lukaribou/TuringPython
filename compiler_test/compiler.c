#define ARRAY_DEFAULT_SIZE 255

typedef struct {
    unsigned int len;
    unsigned int allocated;
} BrideInfo;

typedef struct {
    unsigned int ptr_bride;
    char* bride;
    BrideInfo* bride_info;
} Machine;

// étend (double) la mémoire allouée pour le ruban si nécessaire
void maybe_extend_bride(Machine* m, unsigned int size)
{
    if (m->bride_info->allocated < size)
    {
        m->bride_info->allocated = m->bride_info->allocated << 1;
        // doubler mémoire allouée
        m->bride = realloc(m->bride, sizeof(char) * m->bride_info->allocated);
    }
}

// décale toutes les données derrière et insère le caractère à pos
void bride_insert_at_position(Machine* m, unsigned int pos, char to_insert)
{
    maybe_extend_bride(m, pos);

    for (int i = m->bride_info->len - 1; i >= pos; i--)
    {
        m->bride[i + 1] = m->bride[i];
    }
    m->bride[pos] = to_insert;
    m->bride_info->len += 1;
}

void instruction_left(Machine* m)
{
    m->ptr_bride -= 1;

    if (m->ptr_bride == -1)
    {
        bride_insert_at_position(m, 0, 'b');
        m->ptr_bride = 0;
    }
}

int main(int argc, char* argv[])
{
    BrideInfo bride_info = {
        .len = ARRAY_DEFAULT_SIZE,
        .allocated = ARRAY_DEFAULT_SIZE
    };

    Machine machine = {
        .ptr_bride = 0,
        .bride = malloc(ARRAY_DEFAULT_SIZE * sizeof(char)),
        .bride_info = &bride_info
    };

    free(machine.bride_info);
    free(machine.bride);
}