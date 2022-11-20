module main

struct Machine {
mut:
	ptr_bride u64
	bride	  []string
}

fn instruction_left(mut m &Machine) {
	if m.ptr_bride == 0 {
		m.bride.prepend('b')
		m.ptr_bride = 1
	}
	m.ptr_bride -= 1
}

fn instruction_right(mut m &Machine) {
	m.ptr_bride += 1
	m.bride << 'b'
}

fn instruction_write(mut m &Machine, to_write string) {
	m.bride[m.ptr_bride] = to_write
}

fn instruction_goto(mut m &Machine) {
	// TODO:
}

fn init_machine() Machine {
	return Machine{0, []}
}

fn print_bride(m &Machine) {
	for value in m.bride {
		print(value)
	}
}

fn main() {
	mut m := init_machine()
	m.bride = ['1', '2', '3']
	print_bride(m)
}