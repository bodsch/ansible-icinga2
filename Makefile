#
export TOX_SCENARIO  ?= default
export TOX_ANSIBLE   ?= ansible_7.0

.PHONY: converge destroy verify test lint

default: converge

converge:
	@hooks/converge

destroy:
	@hooks/destroy

verify:
	@hooks/verify

test:
	@hooks/test

lint:
	@hooks/lint
