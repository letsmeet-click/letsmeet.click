test:
	docker-compose up -d
	docker exec -ti letsmeetclick_web_1 py.test 
