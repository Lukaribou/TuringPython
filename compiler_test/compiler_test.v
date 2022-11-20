module main

fn test_left() {
	mut m := init_machine()
	m.ptr_bride = 0
	m.bride = ['0']
	instruction_left(mut m)
	assert m.ptr_bride == 0
	assert m.bride.len == 2
	assert m.bride[0] == 'b'
}

fn test_right() {
	mut m := init_machine()
	m.ptr_bride = 0
	m.bride = ['0']
	instruction_right(mut m)
	assert m.ptr_bride == 1
	assert m.bride.len == 2
	assert m.bride[0] == '0' && m.bride[1] == 'b'
}

fn test_write() {
	mut m := init_machine()
	m.ptr_bride = 0
	m.bride = ['0', '1']
	instruction_write(mut m, '1')
	assert m.bride[0] == '1' && m.bride[1] == '1'
}