# w-c

rule hello_world:
	input: "world.txt"
	output: "hello_world.txt"
	shell:
		" echo 'Hello' | cat - {input} > {output}"