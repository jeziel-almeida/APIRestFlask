rodar:
	flask run
rodar_reload:
	FLASK_DEBUG=1 flask run
rotas:
	flask routes
format:
	blue .
	isort .
lint:
	blue . --check
	isort . --check
getpessoas:
	http get http://localhost:5000/pessoas
headpessoas:
	http head http://localhost:5000/pessoas