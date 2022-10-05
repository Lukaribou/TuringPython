#include <stdlib.h>
#include <stdio.h>

#define ARRAY_DEFAULT_SIZE 1 << 3

typedef struct {
    unsigned int len;
    unsigned int allocated;
} BrideInfo;

typedef struct {
    int ptr_bride;
    char* bride;
    BrideInfo* bride_info;
} Machine;

// étend (double) la mémoire allouée pour le ruban si nécessaire
void bride_extend_if_necessary(Machine* m, unsigned int size)
{
    short int changed = 0;

    while (m->bride_info->allocated < m->bride_info->len + size)
    {
        m->bride_info->allocated = m->bride_info->allocated << 1;
        changed = 1;
    }
    if (changed)
    {
        // doubler mémoire allouée
        m->bride = realloc(m->bride, sizeof(char) * m->bride_info->allocated);
    }
}

// décale toutes les données derrière et insère le caractère à pos
void bride_insert_at_position(Machine* m, unsigned int pos, char to_insert)
{
    bride_extend_if_necessary(m, pos);

    if (m->bride_info->len > 0)
    {
        for (int i = m->bride_info->len; i >= pos; i--)
        {
            printf("%d", i);
            m->bride[i + 1] = m->bride[i];
        }
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

void instruction_right(Machine* m)
{
    m->ptr_bride += 1;

    if (m->ptr_bride == m->bride_info->len)
    {
        bride_insert_at_position(m, m->ptr_bride, 'b');
    }
}

void instruction_write(Machine* m, char to_write)
{
    if (m->bride_info->len == 0)
        m->bride_info->len = 1;
    m->bride[m->ptr_bride] = to_write;
}

// https://stackoverflow.com/questions/9410/how-do-you-pass-a-function-as-a-parameter-in-c
void instruction_goto(Machine* m, void (*next_state)(Machine*))
{
    next_state(m);
}

void bride_print(Machine* m)
{
    printf("Bride: ");
    for (int i = 0; i < m->bride_info->len; i++)
    {
        printf("%c", m->bride[i]);
    }
    printf("\n");
}

int main(int argc, char* argv[])
{
    BrideInfo bride_info = {
        .len = 0,
        .allocated = ARRAY_DEFAULT_SIZE
    };

    Machine machine = {
        .ptr_bride = 0,
        .bride = malloc(ARRAY_DEFAULT_SIZE * sizeof(char)),
        .bride_info = &bride_info
    };

    instruction_write(&machine, '1');
    instruction_right(&machine);
    instruction_write(&machine, '2');
    instruction_left(&machine);
    instruction_left(&machine);
    instruction_write(&machine, 'a');

    bride_print(&machine);

    free(machine.bride_info);
    free(machine.bride);

    return 0;
}