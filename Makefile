build.%: compose.%.yaml
	docker compose -f compose.yaml -f $< up -d --build --force-recreate

test.%: build.%
	sleep 20s
	/bin/bash ./scripts/test/res_code_is_200.sh
	/bin/bash ./scripts/test/res_code_is_200.sh /admin/grafana
	/bin/bash ./scripts/test/res_code_is_200.sh /bunch
	/bin/bash ./scripts/test/all_containers_are_up.sh

clean.%: compose.%.yaml
	docker compose -f compose.yaml -f $< down

clean: clean.dev clean.stg